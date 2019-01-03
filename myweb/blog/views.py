from django.conf import settings
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Blog,BlogType
from .forms import BlogForm
from reading_statistics.utils import set_read_return_response,model_order_by_read_num
from comment.models import Comment  
from comment.forms import CommentForm
# Create your views here.

def paginator_genertor(obj,current_page_num):
    '''
        return a page object append an attribute named display_range
    '''
    try:
        one_page_blog_num = settings.PAGENATOR_BLOG_COUNT
    except Exception as e:
        one_page_blog_num = 10
    try:
        display_list_size = settings.PAGENATOR_DISPLAY_LIST_SIZE
    except Exception as e:
        display_list_size =5
    page_nagitor = Paginator(obj,one_page_blog_num)
    page = page_nagitor.get_page(current_page_num)
    total_page_num = page_nagitor.num_pages
    tatal_blog_num = page_nagitor.count
    current_page_num = page.number
    start = 1
    end = display_list_size
    mid = (start + end)//2
    if current_page_num > mid:
        start = current_page_num
        end = current_page_num + display_list_size - 1
    if end > total_page_num:
        end = total_page_num
        start = total_page_num - display_list_size + 1
    if start < 1 :
        start = 1
    page.display_range = range(start,end+1)
    return page




def blog_filter(filter_field):
    compare_set = set()
    compare_set.add('blogtype')
    available_field = {}
    if len(filter_field):
        for i,v in filter_field.items():
            if i in compare_set:
                available_field[i] = int(v)
    return Blog.objects.filter(**available_field).order_by('-update'),available_field

def generate_args_url(path,fields):
    path += '?' 
    for i,v in fields.items():
        path += '%s=%s;&'%(i,v)
    return path


def show_blog(req):
    context = {}
    current_page_num = req.GET.get('page','')
    blog_list,available_field = blog_filter(req.GET,)
    #缓存获取本月热门博客
    this_month_hot_blog= cache.get('this_month_hot_blog')
    if not this_month_hot_blog:
        this_month_hot_blog = model_order_by_read_num(Blog)
        cache.set('this_month_hot_blog',this_month_hot_blog,3600)
    #得到过滤后的url 以免 与page 参数发生冲突
    context['available_field'] = available_field
    context['args_url'] = generate_args_url(req.path,available_field)
    blogtypes = BlogType.objects.all()    
    page  = paginator_genertor(blog_list,current_page_num)
    blog_list = page.object_list
    context['active_app'] = req.resolver_match.url_name
    context['is_authenticated'] = req.user.is_authenticated
    context['blogs'] = blog_list
    context['page'] = page
    context['blogtypes'] =blogtypes
    context['this_month_hot_blog'] =this_month_hot_blog
    return render(req,'blog/blog.html',context)

@login_required
def write_blog(req):
    context = {}
    if req.method == 'GET':
        blog_form = BlogForm()
        context['blog_form'] = blog_form
        return render(req,'blog/write_blog.html',context)
    else:
        blog_form = BlogForm(req.POST)
        if blog_form.is_valid():
            blog_type_list = blog_form.cleaned_data['blog_type_list']
            blog_theme = blog_form.cleaned_data['theme']
            blog_context = blog_form.cleaned_data['context']
            blog_owner = req.user
            b = Blog.objects.create(
                theme = blog_theme,
                user = blog_owner,
                context = blog_context
            )
            b.blogtype_set.set(blog_type_list)
            return redirect('blog')
        else:
            blog_form = BlogForm(req.POST)
            context[blog_form] = blog_form
            context['erro'] = '**不知道为啥，博客发表失败！'
            return render(req,'blog/write_blog.html',context)



def blog_detail(req,pk):
    context = {}
    blog = get_object_or_404(Blog,pk=pk)
    content_type = ContentType.objects.get_for_model(Blog)
    comments = Comment.objects.filter(
        content_type=content_type,
        object_id=pk,
        parent_comment=None
        )
    current_page_num = req.GET.get('page')
    page  = paginator_genertor(comments,current_page_num)
    comments = page.object_list
    context['page'] = page
    # for comment in comments:
    #     if comment.child_comment.count():
    #         comment.child_reply = comment.child_comment.all()
    context['comments'] = comments
    context['blog'] = blog
    data = {
        'content_type':'blog',
        'object_id':blog.id,
        'parent_comment_id': 0,
    }
    comment_form = CommentForm(initial=data)
    context['comment_form'] = comment_form
    response = set_read_return_response(req,blog,context)
    return response


def filter_blogtype():
    pass

def filter_blog():
    pass
