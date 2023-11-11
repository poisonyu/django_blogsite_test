from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord

register = template.Library()

@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.pk
    if LikeCount.objects.filter(content_type=content_type, object_id=object_id):
        like_count = LikeCount.objects.get(content_type=content_type, object_id=object_id)
        return like_count.liked_num
    else:
        return 0
    

@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    return ContentType.objects.get_for_model(obj).model