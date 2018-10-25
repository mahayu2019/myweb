from django.contrib.contenttypes.models import ContentType
from .models import ReadNum


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):  # 检测cook是否存在,不存在则加1次
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在记录,阅读数增加1
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在记录,关联文章之后计数加1
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

    return key
