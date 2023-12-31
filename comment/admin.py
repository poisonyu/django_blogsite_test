from django.contrib import admin
from .models import Comment

# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'content_type', 'text', 'comment_time', 'user', 'root', 'parent', 'reply_to')

    