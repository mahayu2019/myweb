from django.shortcuts import render_to_response
from read_statistics.utils import get_seven_days_read_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog


# 网站首页
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    return render_to_response('home.html', context=context)
