import threading 
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User 
from django.conf import settings
from django.core.mail import send_mail 
from django.template.loader import render_to_string


#from ckeditor_uploader.fields import RichTextUploadingField
#from django import forms
#from ckeditor.widgets import CKEditorWidget
#from read_statistics.models import Like_Num
# Create your models here.

class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            self.fail_silently,
            html_message=self.text,
        )


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

   # parent_id = models.IntegerField(default=0)
    root = models.ForeignKey('self', related_name="root_comment",null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name="parent_comment", null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    #like_num = GenericRelation(Like_Num)

    def __str__(self):
        return self.text
    
    def send_mail(self):
        if self.parent is None:
            # 评论内容
            subject = '有人评论你的博客'
            #text = comment.text + '/n' + comment.content_object.get_url()
            email = self.content_object.get_email()
            # send_mail(subject, text, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        else:
            # 回复内容
            subject = '有人回复你的博客'         
            email = self.reply_to.email 
        if email != '':
            # text = '%s\n<a href="%s">%s</a>' % (self.text, self.content_object.get_url(), '点击查看')
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_mail.html', context)
            # import pdb 
            # pdb.set_trace()
            send_mail = SendMail(subject, text, email)
            send_mail.start()

    class Meta:
        ordering = ['comment_time']


