from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_personal_center, name='user_personal_center'),
    path('login/', views.acc_login, name='login'),
    path('logout/', views.acc_logout, name='logout'),
    path('register/', views.acc_register, name='register'),
    path('profile_edit/',views.profile_edit,name='profile_edit'),
    path('verification/',views.verification,name='verification'),
]
