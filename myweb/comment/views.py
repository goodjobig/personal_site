from django.shortcuts import render,redirect,HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from blog.models import Blog
from .models import Comment
from .forms import CommentForm
# Create your views here.

def upload_comment(req):
    user = req.user
    referer = req.META.get('HTTP_REFERER',reverse('home'))
    if req.method == 'POST':
        comment_form = CommentForm(req.POST,user=user)
        if comment_form.is_valid():
            comment = Comment()
            comment.content_object = comment_form.cleaned_data['content_object']
            comment.text = comment_form.cleaned_data['text']
            comment.user = comment_form.cleaned_data['user']
            comment.parent_comment = comment_form.cleaned_data['parent_comment']
            comment.save()
            return redirect(referer)
        else:
            return redirect(referer)

def ajax_get_comment(req):
    data = {}
    if req.method == 'GET':
        comment_pk = req.GET.get('comment_pk','')
        comment = Comment.objects.get(pk=comment_pk)
        comments = Comment.objects.filter(parent_comment=comment)
        data['comment_list'] = []
        for comment in comments:
            comment_data = {}
            comment_data['id'] = comment.id
            try:
                name= comment.user.userprofile.nickname
            except Exception as e:
                name = username    
            comment_data['user'] = name 
            comment_data['create_time'] = comment.create_time
            comment_data['text'] =comment.text
            data['comment_list'].append(comment_data)
        # comment_json_data = serializers.serialize('json',comments, fields=('id','user','text','create_time'))
        # return HttpResponse(comment_json_data)
    return JsonResponse(data)
