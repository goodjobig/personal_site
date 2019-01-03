from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from useroperations.models import UserProfile
# Create your models here.

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    text = RichTextUploadingField()
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    parent_comment = models.ForeignKey(
        'Comment',
        on_delete=models.DO_NOTHING,
        null=True,blank=True,
        related_name='child_comment',
        )

    class Meta:
        verbose_name = '评论'
        ordering = ['-create_time']