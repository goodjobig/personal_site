from django import template
from django.template.defaultfilters import truncatechars,safe

register = template.Library()

@register.filter
def editor_safe(value,limit_num):
    return safe(truncatechars(value,limit_num))