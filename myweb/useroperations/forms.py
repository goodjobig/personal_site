from time import time
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User  
from .models import UserProfile
from myweb.widgets import input_factor

def login_form_factor(need_verification,req):
    if req.method == 'GET':
        if not need_verification:
            return LoginForm()
        else:
            return verification_login_form()
    if not need_verification:
        return LoginForm(req.POST)
    else:
        return verification_login_form(req.POST,req=req)


class LoginForm(forms.Form):
    username = forms.fields.CharField(max_length=30,label="用户名",widget=input_factor('TextInput'))
    password = forms.fields.CharField(max_length=30,label="密码",widget=input_factor('PasswordInput'))
    def clean(self):
        return self.cleaned_data

class verification_login_form(forms.Form):
    username = forms.fields.CharField(max_length=30,label="用户名",widget=input_factor('TextInput'))
    password = forms.fields.CharField(max_length=30,label="密码",widget=input_factor('PasswordInput'))
    verification = forms.fields.CharField(max_length=30,label="验证码",widget=input_factor('TextInput',placeholder="请输入验证码"))

    def __init__(self,*args,**kwarg):
        if 'req' in kwarg:
            self.req = kwarg.pop('req')
        super(verification_login_form,self).__init__(*args,**kwarg)

    def clean_verification(self):
        code = self.req.session.get('verification_code')
        u_code = self.cleaned_data['verification']
        if code != u_code:
            raise ValidationError('验证码错误')
        return self.cleaned_data['verification']

    def clean(self):
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.fields.CharField(max_length=30)
    password = forms.fields.CharField(max_length=30)
    confirm_password = forms.fields.CharField(max_length=30)
    email = forms.fields.EmailField(max_length=30)

    def clean(self):
        if self.cleaned_data['password']\
        != self.cleaned_data['confirm_password']:
            raise ValidationError('两次输入密码不一致')
        else:
            self.cleaned_data.pop('confirm_password')

        return self.cleaned_data

class UserProfileEditForm(forms.Form):
    nickname = forms.fields.CharField(
        max_length=30,
        label="昵称",
        widget= input_factor('TextInput'),
    )

    photo = forms.fields.ImageField(
        widget= forms.FileInput(
            # attrs={
            #     'style':'overflow:hidden;width:100%;height:100%;'
            # }
            ),
        )
    number = forms.fields.CharField(
            max_length=11,
            widget=input_factor('NumberInput'),
            validators=[
                RegexValidator(r'^[0-9]{1,11}$', 'Enter a valid phone number.')
            ],
            label='手机号码',
        )
    def __init__(self,*arg,**kwarg):
        if 'user' in kwarg:
            self.user = kwarg.pop('user')
        super(UserProfileEditForm,self).__init__(*arg,**kwarg)


    def clean(self):
        filename = self.cleaned_data['photo'].name
        self.cleaned_data['photo'].name = self.user.username + str(time())+ '.' +filename.split('.')[-1]
        try:
            self.user.userprofile.nickname = self.cleaned_data['nickname']
            self.user.userprofile.photo = self.cleaned_data['photo']
            self.user.userprofile.number = self.cleaned_data['number']
            self.user.userprofile.save()
        except User.userprofile.RelatedObjectDoesNotExist:
            temp = self.cleaned_data
            temp['user'] =self.user
            up = UserProfile.objects.create(**temp)
            if not up:
                raise ValidationError('创建用户失败')
        return self.cleaned_data


