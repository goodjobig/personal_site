from django import template
from collections import Iterable


register = template.Library()

@register.simple_tag
def get_blogtypes(blog):
    blog_types_name = list(blog.blogtype_set.all().values_list('type_name'))
    blog_types_name = [i[0] for i in blog_types_name]
    if isinstance(blog_types_name,Iterable):
        type_list_str = ''.join(blog_types_name)
    else:
        type_list_str= ''
    return type_list_str