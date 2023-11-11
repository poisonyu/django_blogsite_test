from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.utils import timezone

# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpandMethod:
    def get_read_num(self):
        try:
            content_type = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=content_type, object_id=self.id)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0



class ReadDetail(models.Model):
    '''
    用来统计某一段日期的阅读数量'''
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

'''
class CommentNum(models.Moedl):
    comment_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
'''

