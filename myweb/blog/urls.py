from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_blog,name='blog'),
    path('write_blog/',views.write_blog,name='write_blog'),
    path('<int:pk>/',views.blog_detail,name='blog_detail'),
]
