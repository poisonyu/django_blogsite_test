from django.contrib import admin
from .models import Blog, BlogType#, ReadNum
from django.contrib.auth.models import User 

# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'created_time', 'last_updated_time')  #  
    ordering = ('id',)
