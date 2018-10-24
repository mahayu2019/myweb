from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User  # 导入后台系统管理用户
from ckeditor_uploader.fields import RichTextUploadingField


class BlogType(models.Model):  # 博客类型,注意必须放置于blog之前,因为有外键调用
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50)  # 标题
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)  # 类型,引用外键
    content = RichTextUploadingField()  # 内容
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 作者,调用系统管理用户
    created_time = models.DateTimeField(auto_now_add=True)  # 发布时间自动获取当前系统时间
    last_updated_time = models.DateTimeField(auto_now_add=True)


    # 返回阅读数量的值
    '''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:  #阅读计数对象不存在则返回0
            return 0
    '''

    def __str__(self):
        return "<Blog %s>" % self.title

    # 按创建时间倒序排列
    class Meta:
        ordering = ['-created_time']

'''
# 对每篇文章阅读计数
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)  # 统计文章被浏览的次数
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
'''