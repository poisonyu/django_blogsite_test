from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# from django.db.models.fields import exceptions
from django.core import exceptions
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadDetail
from django.urls import reverse 

# Create your models here.


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
    
class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog: %s' % self.title 
    
    def get_url(self):
        return reverse('blog:blog_detail', kwargs={'blog_id': self.pk})

    def get_email(self):
        return self.author.email
    
    class Meta:
        ordering = ['-created_time']

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
'''
    
    