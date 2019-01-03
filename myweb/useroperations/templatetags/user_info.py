from django import template
from django.contrib.auth.models import User
register = template.Library()

def get_userprofile(user):
    '''
        according to the User object return a userprofile object or False
    '''
    try:
        up = user.userprofile
        print('&**********%s'%up)
        return up
    except User.userprofile.RelatedObjectDoesNotExist :
        return False



@register.simple_tag
def get_nickname_or_username(user):
    up = get_userprofile(user)
    if not up:
        return user.username  
    return up.nickname


@register.simple_tag
def get_user_photo_url(user):
    up = get_userprofile(user)
    if not up:
        return ''  
    return up.photo.url