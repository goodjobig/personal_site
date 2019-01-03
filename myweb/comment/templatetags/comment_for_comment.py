from django import template
from django.template.defaultfilters import safe
from ..models import Comment

register = template.Library()

# @register.filter
# def has_child(comment_object):
#     child_num = Comment.objects.filter(parent=comment_object).count()
#     if child_num:
#         comment_object.has_child = True
#     return comment_object


@register.simple_tag
def get_child_comment(comment):    
    child_num = Comment.objects.filter(parent_comment=comment).count()
    if child_num:
        return safe('<a href="javascript:;" onclick="ajax_get_comment(%d,this)">更多</a>'%comment.id)
    else:
        return ''