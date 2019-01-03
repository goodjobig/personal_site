from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from reading_statistics.utils import GetReadInfo
from ckeditor_uploader.fields import RichTextUploadingField
from reading_statistics.models import ReadCount
# Create your models here.

# class BlogManager(models.Manager):
#     def __init__(self,*args,**kwargs):
#         super(BlogManager,self).__init__(*args,**kwargs)

class Blog(models.Model,GetReadInfo):
    """docstring for Blog"""
    theme = models.CharField(max_length=60,default='无主题',verbose_name = '主题')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='博主')
    update = models.DateTimeField(verbose_name='更新时间',auto_now_add=True)
    context = RichTextUploadingField(max_length = 500,null=True,blank=True)
    read_statistics = GenericRelation(ReadCount)
    # comments = models.ForeignKey('Blog',null=True,blank=True,on_delete=models.SET_NULL)
    # like = models.ForeignKey('Like',null=True,blank=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = '博客'
        ordering = ['-update']


class BlogType(models.Model):
    type_name = models.CharField(max_length=60,verbose_name='博客类型')
    blog = models.ManyToManyField(Blog,blank=True)

    def __str__(self):
        return self.type_name
    