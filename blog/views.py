from django.shortcuts import render_to_response, get_object_or_404
from .models import BlogType, Blog
from django.core.paginator import Paginator  # 分页器
from django.conf import settings  # 引用配置文件
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read

context = {}


# 公共方法
def get_blog_list_common_data(request, blog_all_list):
    paginator = Paginator(blog_all_list, settings.EACG_PAGE_BLOGS_NUMBER)  # 每页n条数据,数值写于配置文件的自定义参数中
    page_num = request.GET.get('page', 1)  # 获取页码参数(Get请求)
    page_of_blogs = paginator.get_page(page_num)  # 自动处理获得的参数,非法参数默认为1
    currentr_page_num = page_of_blogs.number  # 获取当前页码
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num,
                            min(currentr_page_num + 2, paginator.num_pages) + 1))  # paginator.num_pages-->总页数
    # 首尾页间隔省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 显示头尾数链接
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取每个分类的对应数量
    blog_types_list = BlogType.objects.annotate(blog_count=Count('blog'))  # 下部注释部分代码与此等价


    # 按日期分类统计
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = blog_types_list
    #  context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")  # 按日期分类
    context['blog_dates'] = blog_dates_dict
    return context


# 文章列表
def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blog_all_list)
    return render_to_response('blog_list.html', context)


# 具体博文内容
def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)  # 根据传入主键值,检索对应内容
    read_cookie_key = read_statistics_once_read(request, blog)

    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()  # 上一条
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 下一条
    context['blog'] = blog

    response = render_to_response('blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # 设置cook标记已读,退出浏览器后失效
    return response


# 博客分类链接
def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blog_with_type.html', context)


# 按日期分类
def blog_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('blog_with_date.html', context)
