import string
import random
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import logout,login,authenticate
from django.core.mail import send_mail
from django.views.decorators.http import require_POST,require_http_methods,require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm,RegisterForm,UserProfileEditForm
from .models import UserProfile
from .forms import login_form_factor
# Create your views here.
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def verification(req):
    s = string.ascii_letters + string.digits
    c = random.sample(s,4)
    code = ''.join(c)
    print(code)
    width = 120
    height = 40
    def rgb_random():
        return (random.randint(60, 255), random.randint(10, 255), random.randint(64, 255))
    img = Image.new(mode="RGB", size=(width, height), color="white")
    draw = ImageDraw.Draw(img, "RGB")
    font = ImageFont.truetype("static/fonts/aaa.ttf", 25)
    for i,v in enumerate(c):  # 生成5位数的随机字符
        # random_num = str(random.randint(0, 9))  # 随机数字
        # random_lower = chr(random.randint(65, 90))  # 随机小写字母
        # random_upper = chr(random.randint(97, 122))  # 随机小写字母
        # random_char = random.choice([random_num, random_lower, random_upper])  # 随机选择
        # draw.text([5 + i * 24, 10], random_char, rndColor(), font=font)
    # 这里列表里的两个参数表示横纵坐标，在img里面的,第二个参数表示文本内容，第三个是颜色，第四个是字体大小
        draw.text([5 + i * 24, 10], v, rgb_random(),font=font)
    for i in range(100):  # 加噪点
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rgb_random())
    # 加干扰线,这里通过添加多组横纵坐标实现
    for i,v in enumerate(c):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        x3 = random.randint(0, width)
        y3 = random.randint(0, height)
        draw.line((x1, y1, x2, y2, x3, y3), fill=rgb_random())
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    req.session.set_expiry(60)
    req.session['verification_code'] = code
    return HttpResponse(data)

def get_next_failtimes(cookies,key):
    value = cookies.get(key,.0)
    value = int(value)
    if value < 4:
        value += 1   
    return value

@require_http_methods(['POST','GET'])
def acc_login(req):
    context = {}
    key = 'require_login_failtimes'
    failtimes = get_next_failtimes(req.COOKIES,key)
    need_verification = False
    if not failtimes < 4:
        need_verification = True
    form = login_form_factor(need_verification,req)
    context['form'] = form
    if req.method == 'GET':
        return render(req,'user/login.html',context)
    else:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(req,user)
                if not failtimes < 4:
                    if user.email:
                        try:
                            send_mail(
                                '异常登录提醒',
                                '尊敬的%s你好,您在%s有异常登录请确认账号是否存在安全隐患！'%user.username,
                                '283541784@qq.com',
                                ['283541784@qq.com'],
                            )
                        except Exception as e:
                            pass
                return redirect('home')
        context['errors'] = form.errors		
        response = render(req,'user/login.html',context)
        response.set_cookie(key,failtimes)
        return response


@require_GET
def acc_logout(req):
    logout(req)
    return redirect('login')

@require_http_methods(['POST','GET'])
def acc_register(req):
    context= {}
    if req.method == 'GET':
        return render(req,'user/register.html')
    else:
        form = RegisterForm(req.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(**form.cleaned_data)
            except Exception as e:
                context['erro'] ='注册错误'
                return render(req,'user/register.html',context)
            else:
                user.save()
                login(req,user)
            return redirect('blog')
        return render(req,'user/register.html',context)

@require_GET        
@login_required
def user_personal_center(req):
    context = {}
    return render(req,'user/user_personal_center.html',context)

@login_required
def profile_edit(req):
    context = {}
    if req.method == 'GET':
        try:
            up = req.user.userprofile
            initial = {
                'nickname':up.nickname,
                'number':up.number,
            }
            profile_form = UserProfileEditForm(initial=initial)
        except User.userprofile.RelatedObjectDoesNotExist:
            profile_form = UserProfileEditForm()
        context['profile_form'] = profile_form
    else:
        profile_form = UserProfileEditForm(req.POST,req.FILES,user=req.user)
        if profile_form.is_valid():
            return HttpResponse('<script>settimeout(window.location.reload(),3)</script>')
        else:
            context['profile_form'] = profile_form
    return render(req,'user/profile_edit.html',context)
