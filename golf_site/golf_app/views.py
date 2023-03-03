# from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import TeamForm
from .models import BlogPost, Golfer, Team

# Create your views here.

def index(request):

    return render(request, 'base.html')


def blog(request):

    posts = BlogPost.objects.order_by('-timestamp') [0:3]
    page_content = {
        'posts': posts,
    }

    return render(request, 'golf_app/blog.html', page_content)


def build_team(request):
    if request.POST:
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(standings)
    #return render(request, 'golf_app/build_team.html', {'form': form})
    return render(request, 'golf_app/build_team.html', {'form': TeamForm})


def standings(request):

    teams = Team.objects.order_by('-team_points')
    teams_list = {
        'teams': teams,
    }

    return render(request, 'golf_app/standings.html', teams_list)