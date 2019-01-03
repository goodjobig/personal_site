from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django import forms
from django.db.models import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Comment

class CommentForm(forms.Form):
    content_type = forms.fields.CharField(max_length=30,widget=forms.fields.HiddenInput)
    object_id = forms.fields.IntegerField(widget=forms.fields.HiddenInput)
    text = forms.fields.CharField(
        label=False,
        widget=CKEditorUploadingWidget(
            attrs={'class':'form-control',},
            config_name ='comment_ckeditor',
            ),
        )
    # text = RichTextUploadingFormField(label=False,widget=forms.Textarea(attrs={'class':'form-control',}))
    parent_comment_id  = forms.fields.IntegerField(
        widget=forms.fields.HiddenInput(attrs={'id':'parent_comment_id'})
        )

    def __init__(self,*args,**kwargs):
        if kwargs.get('user'):
            self.user = kwargs.pop('user')
        super(CommentForm,self).__init__(*args,**kwargs)

    def clean(self):
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise ValidationError('无效登录')
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            obj = model_class.objects.get(id=object_id)
            self.cleaned_data['content_object'] = obj
        except ObjectDoesNotExist as e:
            raise ValidationError('博客不存在无法评论')
        if self.cleaned_data['parent_comment_id']:
            self.cleaned_data['parent_comment'] = Comment.objects.get(id=self.cleaned_data['parent_comment_id'])
        else:
            self.cleaned_data['parent_comment'] = None
        return self.cleaned_data