import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):  # 检测cook是否存在,不存在则加1次
        # 总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数+1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()

    return key


# 统计7天内的阅读数量
def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []  # 保存统计数据到列表
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)  # 检索指定日期的数据
        result = read_details.aggregate(read_num_sum=Sum('read_num'))  # 对指定日期的结果集中求和
        read_nums.append(result['read_num_sum'] or 0)  # 数值为None时用0代替显示
    return dates, read_nums  # 注意此处返回顺序影响图标控件显示顺序


# 今日热门阅读
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today) \
        .order_by('-read_num')  # 检索当天阅读数据,按阅读量倒序
    return read_details[:7]  # 取最新的7个数据


# 昨日热门阅读
def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday) \
        .order_by('-read_num')  # 检索当天阅读数据,按阅读量倒序
    return read_details[:7]  # 取最新的7个数据


# 本周热门
def get_7_days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects \
        .filter(content_type=content_type, date__lt=today, date__gt=date) \
        .values('content_type', 'object_id') \
        .annotate(read_num_sum=Sum('read_num')) \
        .order_by('-read_num')
    return read_details[:7]
