import datetime
from unittest import result
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum 

def read_statistics_once_read(request, obj):
    content_type = ContentType.objects.get_for_model(obj)
    key = f'{content_type.model}_{obj.pk}_read'

    if not request.COOKIES.get(key):
        '''
        if ReadNum.objects.filter(content_type=content_type, object_id=obj.id).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=content_type, object_id=obj.id)
        else:
            # 不存在对应记录
            readnum = ReadNum(content_type=content_type, object_id=obj.id)
        '''
        readnum, created = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.id)
        # 计数
        readnum.read_num += 1
        readnum.save()
        date = timezone.now().date()
        '''
        if ReadDetail.objects.filter(content_type=content_type, object_id=obj.id, date=date):
            readdetail = ReadDetail.objects.get(content_type=content_type, object_id=obj.id, date=date)
        else:
            readdetail = ReadDetail(content_type=content_type, object_id=obj.id, date=date)
        '''
        readdetail, created = ReadDetail.objects.get_or_create(content_type=content_type, object_id=obj.id, date=date)
        readdetail.read_num += 1
        readdetail.save()
    return key 

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_detail.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]

def get_senven_days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects \
        .filter(content_type=content_type, date__lt=today, date__gt=date) \
        .values('content_type', 'object_id') \
        .annotate(read_num_sum=Sum('read_num')) \
        .order_by('-read_num_sum')
    return read_details[:7]



