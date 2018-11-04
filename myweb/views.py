from django.shortcuts import render, redirect
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth  # from django.contrib.auth import login 因为有login同名方法,所以引用上一层
from django.urls import reverse
from .forms import LoginForm

context = {}


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')  # 筛选时间范围
    return blogs


# 网站首页
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 缓存7天热门博客的数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)  # 获得数据存入缓存,计时单位秒

    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs
    return render(request, 'home.html', context=context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)  # 注意此处的login是auth里的login
            return redirect(request.GET.get('from', reverse('home')))  # 反转异常?

    else:
        login_form = LoginForm()

    context['login_form'] = login_form
    return render(request, 'login.html', context)
