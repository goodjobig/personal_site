from django.contrib import admin
from .models import ReadCount
# Register your models here.
@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    list_display = ('id','read_count','content_type','object_id')