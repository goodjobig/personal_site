# from django.db.models.fields import exceptions as db_e
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from .models import ReadCount

class GetReadInfo():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            rm = ReadCount.objects.get(content_type=ct,object_id=self.id)
            return rm.read_count
        except Exception as e:
            return 0


            
def set_read_return_response(req,blog,context):
    key = 'blog_%s_reades' % blog.id
    if not req.COOKIES.get(key):
        try:
            ct = ContentType.objects.get_for_model(blog)
            read = ReadCount.objects.get(content_type=ct,object_id=blog.id)
            read.read_count += 1
            read.create_time = timezone.now()
        except Exception as e:
            ct = ContentType.objects.get_for_model(blog)
            read = ReadCount.objects.create(content_type=ct,object_id=blog.id,read_count=1)
        read.save()
        response = render(req,'blog/detail.html',context)
        response.set_cookie(key,'true')
        return response
    else:
        response =render(req,'blog/detail.html',context)
        return response


def model_order_by_read_num(model):
    '''
        give a model return a read statistic TOP 10 models list
    '''
    today = timezone.now().today()
    m = today.month
    y = today.year
    month_start_day = timezone.datetime(year=y,month=m,day=1)
    objs = model.objects.filter(read_statistics__create_time__gt=month_start_day)\
                .order_by('-read_statistics__read_count')\
                .values('id','theme','read_statistics__read_count')
    return objs

def get_read_quantity_in_days(model,days):
    days = range(1,days+1)
    today = timezone.now().date()
    quantity = []
    dates = []
    for day in days:
        date = today - timezone.timedelta(days=day)
        dates.append(date.strftime('%m/%d'))
        ct = ContentType.objects.get_for_model(model)
        res = ReadCount.objects.filter(content_type=ct,create_time=date).aggregate(read_quantity=Sum('read_count'))
        quantity.append(res['read_quantity'] or 0)
    return dates[::-1],quantity[::-1]
