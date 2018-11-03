from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),  # 博客列表
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blog_with_type, name='blog_with_type'),  # 类别分类
    path('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),  # 日期分类
]
