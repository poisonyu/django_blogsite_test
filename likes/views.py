from django.shortcuts import render
from .models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType 
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def ErrorResponse(code, message):
    data = {}
    data['code'] = code 
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')
    
    model = request.GET.get('model')
    object_id = request.GET.get('object_id')

    try:
        content_type = ContentType.objects.get(model=model)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    if request.GET.get('is_like') == 'true':
        # 点赞
        like_record, created = LikeRecord.objects.get_or_create(user=user, content_type=content_type, object_id=object_id)
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            #已经点赞过
            return ErrorResponse(402, 'repeate like')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数-1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            return ErrorResponse(402, 'yet like it')
        
