"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings 
from django.conf.urls.static import static
#from useroperations import views as u_views
from like.views import like_change
from . import views
urlpatterns = [
    path('', views.home_page,name='home'),
    path('graph_info/', views.graph_info,name='graph_info'),
    path('admin/', admin.site.urls),
    path('like_change/', like_change,name='like_change'),
    path('blog/', include('blog.urls')),
    # path('login/',u_views.acc_login,name='login'),
    # path('logout/',u_views.acc_logout,name='logout'),
    # path('register/',u_views.acc_register,name='register'),
    path('user/',include('useroperations.urls')),
    path('comment/', include('comment.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
