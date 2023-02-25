# from django.http import HttpResponse
from django.shortcuts import render
from .models import BlogPost

# Create your views here.

def index(request):

    # return HttpResponse("<h1> Text Homepage <h1>")
    return render(request, 'base.html')

def blog(request):

    posts = BlogPost.objects.order_by('-timestamp') [0:3]
    page_content = {
        'posts': posts,
    }

    return render(request, 'blog.html', page_content)