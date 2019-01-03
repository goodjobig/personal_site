from django.db import models
from django.contrib.auth.models import User
from blog.models import Blog

# Create your models here.

class UserProfile(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30,verbose_name='昵称')
    photo = models.ImageField(upload_to='userImage/',default='userImage/default_photo.jpg')
    collect = models.ManyToManyField(Blog,blank=True)
    number = models.CharField(max_length=11)

    class Meta:
        verbose_name = '用户信息'

    def __str__(self):
        return self.nickname

# @property
# def get_username_or_nickname(self):
#     if self.userprofile.nickname:
#         return self.userprofile.nickname
#     return self.username

# User.get_username_or_nickname = get_username_or_nickname