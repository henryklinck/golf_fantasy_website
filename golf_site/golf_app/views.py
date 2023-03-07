# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import TeamForm
from django.contrib import messages

from .models import BlogPost, Golfer, Team, SeasonSettings

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
            if (form.instance.password_used == SeasonSettings.objects.first().user_password):
                form.save()
                return redirect(standings)
            else:
                messages.info(request, 'Your password is incorrect')
    return render(request, 'golf_app/build_team.html', {'form': TeamForm})


def standings(request):

    teams = Team.objects.order_by('-team_points')
    teams_list = {
        'teams': teams,
    }

    return render(request, 'golf_app/standings.html', teams_list)