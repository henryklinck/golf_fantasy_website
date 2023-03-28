# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import TeamForm
from django.contrib import messages
from .update_players import get_curr_player_csv, updates_players
from .models import Golfer, Team
#from django.views.decorators.csrf import csrf_exempt

from .models import BlogPost, Golfer, Team, SeasonSettings

# Create your views here.

def index(request):

    return render(request, 'base.html')


def blog(request):

    posts = BlogPost.objects.order_by('-timestamp') [0:3]
    page_content = {
        'posts': posts,
    }

    player_df = get_curr_player_csv()

    updates_players(player_df)

    return render(request, 'golf_app/blog.html', page_content)


def build_team(request):
    if request.POST:
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            if (team_form.instance.password_used == SeasonSettings.objects.first().user_password):
                team_form.save()
                return redirect(standings)
            else:
                messages.info(request, 'Your password is incorrect')
        
    return render(request, 'golf_app/build_team.html', {'team_form': TeamForm})


def standings(request):

    for team in Team.objects.all():
        team_pts_so_far = 0
        for golfer in team.team_golfers.all():
            team_pts_so_far += golfer.point
        team.team_points = team_pts_so_far

    teams = Team.objects.order_by('-team_points')
    teams_list = {
        'teams': teams,
    }

    return render(request, 'golf_app/standings.html', teams_list)