from django.http import JsonResponse
from django.shortcuts import render_to_response,render
from django.core.cache import cache
from reading_statistics.utils import get_read_quantity_in_days
from blog.models import Blog


def home_page(req):
    context = {}
    context['user'] = req.user
    context['active_app'] = req.resolver_match.url_name
    return render_to_response('index.html',context)

def graph_info(req):
    data = {}
    if cache.get('read_quantity') and cache.get('dates'):
        data['read_quantity'],data['dates'] = cache.get('read_quantity'),cache.get('dates')
    else:
        data['read_quantity'],data['dates'] = get_read_quantity_in_days(Blog,7)
        cache.set('read_quantity',data['read_quantity'])
        cache.set('dates',data['dates'])
    return JsonResponse(data)