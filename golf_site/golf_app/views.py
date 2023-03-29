# from django.http import HttpResponse
#from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import TeamForm, ConfmForm
from django.contrib import messages
from .update_players import get_curr_player_csv, updates_players
from .models import Golfer, Team, SeasonSettings
from .update_players import get_curr_player_csv, initalize_players
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

    return render(request, 'golf_app/blog.html', page_content)


def build_team(request):
    if request.POST:
        team_form = TeamForm(request.POST)

        if team_form.is_valid():
            if (team_form.instance.password_used == SeasonSettings.objects.first().user_password):
                team_form.save()
                curr_team = Team.objects.get(team_name=team_form.instance.team_name)
                #curr_team.creation_time(timezone.now())

                curr_spent = 0
                team_players = set()
                for golfer in curr_team.team_golfers.all():
                    curr_spent += golfer.player_cost
                    team_players.add(golfer.name)
                
                

                # Check if team cost > max budget:

                return render(request, 'golf_app/confm_team.html', 
                {'confm_form': ConfmForm, 
                'confm_name': team_form.instance.team_name,
                'confm_owner': team_form.instance.team_owner,
                'confm_team_cost': str(curr_spent),
                'confm_golfers': team_players
                })
            else:
                messages.info(request, 'Your password is incorrect')

    max_budget = str(SeasonSettings.objects.first().team_budget)    
    return render(request, 'golf_app/build_team.html', {'team_form': TeamForm,
                                                        'max_budget': max_budget,})


def confm_team(request):
    if request.POST:
        confirm_form = ConfmForm(request.POST)

        if confirm_form.is_valid():
            del_team = confirm_form.result()
            if(len(del_team) > 1):
                for team in Team.objects.all():
                    if team.team_name == del_team:
                        Team.objects.filter(team_name=del_team).delete()
                        return render(request, 'golf_app/build_team.html', {'messages': str('Your Team Has Been Deleted Successfully')})
    return render(request, 'golf_app/build_team.html')



def standings(request):
    current_stage = SeasonSettings.objects.first().curr_stage
    print("TEST")
    if (current_stage != 'pre' and current_stage != 'init_tourn'):

        current_stage = SeasonSettings.objects.first().curr_stage

        points_df = get_curr_player_csv()

        if (current_stage == 'r_1'):
            print("TEST!!")
            round = {}
            round['r1'] = True
            updates_players(points_df, 'R1')

        elif (current_stage == 'r_2'):
            round = {}
            round['r2'] = True
            updates_players(points_df, 'R2')

        elif (current_stage == 'r_3'):
            round = {}
            round['r3'] = True
            updates_players(points_df, 'R3')

        elif (current_stage == 'r_4'):
            round = {}
            round['r4'] = True
            updates_players(points_df, 'R4')

        print("TEST!")
        for team in Team.objects.all():
            # Get Team's Current Points
            # Check if Team is Cut
            team_pts_so_far = 0
            for golfer in team.team_golfers.all():
                team_pts_so_far += golfer.point
            team.team_points = team_pts_so_far
            

            team.save()
            print(str(team.team_points) + " hi")

        teams = Team.objects.filter(cut=False).order_by('team_points')
        cut_teams = Team.objects.filter(cut=True).order_by('team_points')
        teams_list = {
            'teams': teams,
            'cut_teams' : cut_teams
        }

        return render(request, 'golf_app/standings.html', teams_list)

    elif (current_stage == 'init_tourn' and Golfer.objects.count() < 10):
        print("TEST")

        curr_df = get_curr_player_csv()
        initalize_players(curr_df )
        return render(request, 'golf_app/standings.html', {})

    else:
        return render(request, 'golf_app/standings.html', {})