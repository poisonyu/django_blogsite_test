from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
from django.conf import settings
from comment.models import Comment 
from comment.forms import CommentForm 
#from user.forms import LoginForm
# Create your views here.

def blog_list(request):
    page_num = request.GET.get('page', 1) # 获取URL页码参数
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 分页
    page_of_blogs = paginator.get_page(page_num)
    context = {}
    context['elided_page'] = paginator.get_elided_page_range(page_of_blogs.number, on_each_side=2, on_ends=1)
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = Blog.objects.all()
    context['all_blog_type'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_id):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_id)
    read_cookie_key = read_statistics_once_read(request, blog)
    # content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=content_type, object_id=blog_id, parent=None)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    #context['login_form'] = LoginForm()
    # context['comments'] = comments.order_by('-comment_time')
    # context['comment_count'] = Comment.objects.filter(content_type=content_type, object_id=blog_id).count()
    # context['comment_form'] = CommentForm(initial={'content_type': content_type.model, 'object_id': blog_id, 'reply_comment_id': 0})
    # context['user'] = request.user
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'ture')
    return response

def blog_with_type(request, blog_type_id):
    page_num = request.GET.get('page', 1)
    blog_type = get_object_or_404(BlogType, pk=blog_type_id)
    blogs = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs, settings.EACH_PAGE_BLOGS_NUMBER)
    page_of_blogs = paginator.get_page(page_num)
    elided_page = paginator.get_elided_page_range(page_of_blogs.number, on_each_side=1, on_ends=1)
    context = {}
    
    context['blog_type'] = blog_type
    context['page_of_blogs'] = page_of_blogs
    context['all_blog_type'] = BlogType.objects.all()
    context['elided_page'] = elided_page
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    return render(request, 'blog/blog_with_type.html', context)

def blogs_with_date(request, year, month):
    page_num = request.GET.get('page', 1)
    blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    paginator = Paginator(blogs, settings.EACH_PAGE_BLOGS_NUMBER)
    page_of_blogs = paginator.get_page(page_num)
    context = {}
    context['elided_page'] = paginator.get_elided_page_range(page_of_blogs.number, on_each_side=2, on_ends=1)
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    context['blog_date'] = f'{year}年{month}月'
    context['all_blog_type'] = BlogType.objects.all()
    context['page_of_blogs'] = page_of_blogs
    return render(request, 'blog/blog_with_date.html', context)