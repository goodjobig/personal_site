from django.contrib import admin
from . import models
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    """docstring for BlogAdmin"""
    list_display = ('id','theme','update','get_read_num','user')
    list_filter = ('id','theme','update',)
    class Meta:
        ordering = ['-update']


@admin.register(models.BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

    def count_related_blog(self):
        self.blog_num = models.BlogType.objects.select_related('blog').count()
        return self.blog_num

admin.site.register(models.Blog,BlogAdmin)
