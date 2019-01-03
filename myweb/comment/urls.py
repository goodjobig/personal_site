from django.urls import path
from . import views


urlpatterns = [
    path('upload_comment',views.upload_comment,name='upload_comment'),
    path('ajax_get_comment',views.ajax_get_comment,name='ajax_get_comment'),
]