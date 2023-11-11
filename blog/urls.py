from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('categroy/<int:blog_type_id>/', views.blog_with_type, name='blog_with_type'),
    path('date/<int:year>/<int:month>/', views.blogs_with_date, name='blogs_with_date'),

]