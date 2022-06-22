from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic.base import View
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render

from app.forms import CommentForm
from .models import Menu, Post, Page, Setting


def HomeView(request):
    settings = Setting.objects
    posts = Post.objects.filter(cat_id=1)
    menus = Menu.objects.all()
    products = Post.objects.filter(cat_id=2)
    about = Post.objects.filter(cat_id=3)
    section1_url = settings.get(name='section1-video-url').config
    section2_image_url = settings.get(name='section2-image-url').config
   
    context = {
        'section1_url':section1_url,
        'section2_image_url':section2_image_url,
        'posts':posts,
        'menus':menus,
        'products':products,
        'about':about,

    }
        
    return render(request, 'home.html', context)

def BlogDetailView(request, slug):
    menus = Menu.objects.all()
    posts = Post.objects.filter(cat_id=1)
    blog_post = get_object_or_404(Post.objects.filter(cat_id=1, slug=slug))
    context = {
        'blog_post':blog_post,
        'posts':posts,
        'menus':menus,
        
    }
  
    return render(request, 'blog-details.html', context)

    # return render(request, 'blog-details2.html', context)

def PageView(request, slug):
    menus = Menu.objects.all()
    page = Page.objects.get(slug=slug)

    context = {
        'page':page,
        'menus':menus,   
    }

    return render(request, 'page.html', context)

def Searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Post.objects.all().filter(title__contains=search)
        menus = Menu.objects.all()
        context = {
            'post':post,
            'menus':menus,   
        }
        return render (request, 'searchbar.html', context)

class CommentView(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
           form = form.save(commit=False)
           form.post = post
           form.save()  
        return redirect(post.get_absolute_url())