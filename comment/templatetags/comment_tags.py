from django import template 
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm 
from read_statistics.models import ReadNum
from django.core import exceptions

register = template.Library()

@register.simple_tag
def test(a):
    return 'test' + a


@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id =obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj).model
    comment_form = CommentForm(initial={
        'content_type': content_type,
        'object_id': obj.pk,
        'reply_comment_id': 0
    })
    return comment_form

@register.simple_tag
def get_comments_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None).order_by('-comment_time')

@register.simple_tag
def get_read_num(obj):
    try:
        content_type = ContentType.objects.get_for_model(obj)
        return ReadNum.objects.get(content_type=content_type, object_id=obj.pk).read_num
    except exceptions.ObjectDoesNotExist:
        return 0
