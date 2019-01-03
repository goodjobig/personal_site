from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class ReadCount(models.Model):
    read_count = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # create_time = models.DateField(default=timezone.now())
    create_time = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = '浏览计数'