from django.db import models
from django.contrib.auth.models import User  # 导入后台系统管理用户
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):  # 博客类型,注意必须放置于blog之前,因为有外键调用
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):  # ReadNumExpandMethod 此处属于继承模式
    title = models.CharField(max_length=50)  # 标题
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)  # 类型,引用外键
    content = RichTextUploadingField()  # 内容
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 作者,调用系统管理用户
    created_time = models.DateTimeField(auto_now_add=True)  # 发布时间自动获取当前系统时间
    last_updated_time = models.DateTimeField(auto_now_add=True)
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return "<Blog %s>" % self.title

    # 按创建时间倒序排列
    class Meta:
        ordering = ['-created_time']
