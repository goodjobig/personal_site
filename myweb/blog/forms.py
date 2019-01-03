from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import BlogType
from myweb.widgets import input_factor

class BlogForm(forms.Form):
    blog_type_query = BlogType.objects.all().values('id','type_name')
    blog_type_choice = []
    for i in blog_type_query:
        blog_type_choice.append((i['id'],i['type_name']))
    blog_type = forms.fields.MultipleChoiceField(label='博客类型',choices=blog_type_choice,widget=input_factor('CheckboxSelectMultiple',cls_name=''))
    theme = forms.fields.CharField(label='主题',max_length=128,widget=input_factor('TextInput'))
    context = forms.fields.CharField(
        label='博客内容',
        max_length=255,
        widget= CKEditorUploadingWidget(attrs={'class': 'form-control',},config_name='comment_ckeditor',)
    )

    def __init__(self,*args,**kwargs):
        super(BlogForm,self).__init__(*args,**kwargs)

    def clean_blog_type(self):
        '''
            this function need to be perfect
        '''
        blog_type_id_list = self.cleaned_data['blog_type']
        self.cleaned_data['blog_type_list'] = []
        for blog_type_id in blog_type_id_list:
            #waste a lot of RAM
            if BlogType.objects.get(id=blog_type_id):
                self.cleaned_data['blog_type_list'].append(BlogType.objects.get(id=blog_type_id))
            else:
                ValidationError('请勿绕过页面访问该页！')
        return self.cleaned_data['blog_type']

    def clean(self):
        return self.cleaned_data


