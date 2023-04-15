# from django.http import HttpResponse
#from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import TeamForm, ConfmForm
from django.contrib import messages
from .update_players import get_curr_player_csv, updates_players, check_cut
from .models import Golfer, Team, SeasonSettings
from .update_players import get_curr_player_csv, initalize_players, team_score
from .get_points import get_curr_player_df, update_cut_players, check_cut, get_team_score
from .player_prices import update_player_prices

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
    
    # Submit Team is Clicked
    if request.method=='POST' and 'btnform1' in request.POST:
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            password = team_form.cleaned_data['password_used']

            # Check if Entered Password is Correct
            if (password == SeasonSettings.objects.first().user_password):

                name = team_form.cleaned_data['team_name']
                owner = team_form.cleaned_data['team_owner']
                golfers = team_form.cleaned_data['team_golfers']

                curr_spent = 0
                team_players = set()
                for golfer in golfers:
                    curr_spent += golfer.player_cost
                    team_players.add(golfer.name)
                
                # Check if Team Cost > Max Budget
                if (curr_spent > int(SeasonSettings.objects.first().team_budget)):
                    messages.info(request, 'This Team Value Surpasses Max Budget')

                    
                    # Load Page With Current Form Inputs
                    temp_team = Team.objects.create(team_name=name, team_owner=owner, team_cost=curr_spent)

                    for golfer in golfers:
                        temp_team.team_golfers.add(golfer)

                    form2 = Team.objects.get(team_name=name)  
                    form1 = TeamForm(instance=form2)

                    Team.objects.get(team_name=team_form.instance.team_name).delete()

                    max_budget = int(SeasonSettings.objects.first().team_budget) 
                    formatted_max_budget = inttocommas(max_budget)

                    return render(request, 'golf_app/build_team.html', {'team_form': form1,
                                                                'max_budget': formatted_max_budget,})
    

                temp_team = Team.objects.create(team_name=name, team_owner=owner, team_cost=curr_spent)

                for golfer in golfers:
                    temp_team.team_golfers.add(golfer)

                form2 = Team.objects.get(team_name=name)  
                conf_form = ConfmForm(instance=form2)

                Team.objects.get(team_name=name).delete()

                return render(request, 'golf_app/confm_team.html', 
                    {
                    'confm_form': conf_form, 
                    'confm_name': name,
                    'confm_owner': owner,
                    'confm_team_cost': inttocommas(curr_spent),
                    'confm_golfers': team_players,
                    'false' : False
                    })

            else:
                # Wrong Password Entered
                messages.info(request, 'Your password is incorrect')

    # Calculate Cost Button is Clicked
    elif request.method=='POST' and 'btnform2' in request.POST:
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            total_cost = 0
            team_form.save()
            curr_team = Team.objects.get(team_name=team_form.instance.team_name)

            total_cost = 0
            for golfer in curr_team.team_golfers.all():
                total_cost += golfer.player_cost
            
            formatted_total_cost = inttocommas(total_cost)

            # Print Total Cost
            if total_cost > SeasonSettings.objects.first().team_budget:
                messages.info(request, 'Over Budget - Current Cost is: $' + formatted_total_cost)
            else:
                messages.info(request, 'Under Budget - Current Cost is: $' + formatted_total_cost)

            # Load Page With Current Form Inputs
            team_name1 = team_form.instance.team_name
            form2 = Team.objects.get(team_name=team_name1)  
            form1 = TeamForm(instance=form2)

            Team.objects.get(team_name=team_form.instance.team_name).delete()

            max_budget = int(SeasonSettings.objects.first().team_budget) 
            formatted_max_budget = inttocommas(max_budget)

            return render(request, 'golf_app/build_team.html', {'team_form': form1,
                                                        'max_budget': formatted_max_budget,})

    # If No Clicks, Load Empty Page
    max_budget = int(SeasonSettings.objects.first().team_budget) 
    formatted_max_budget = inttocommas(max_budget)
    return render(request, 'golf_app/build_team.html', {'team_form': TeamForm(),
                                                        'max_budget': formatted_max_budget,})


def confm_team(request):
    if request.POST:
        confirm_form = ConfmForm(request.POST)

        if confirm_form.is_valid():
            name = confirm_form.cleaned_data['team_name']
            owner = confirm_form.cleaned_data['team_owner']
            golfers = confirm_form.cleaned_data['team_golfers']
            cost = confirm_form.cleaned_data['team_cost']

            temp_team = Team.objects.create(team_name=name, team_owner=owner, team_cost=cost)

            for golfer in golfers:
                temp_team.team_golfers.add(golfer)
            
            return redirect("build_team")

    return render(request, 'golf_app/build_team.html')



def standings(request):

    curr_csv = get_curr_player_csv()

    for team in Team.objects.all():
        golfers = set()
        for golfer in team.team_golfers.all():
            golfers.add(golfer.name)
    
        score = team_score(golfers, curr_csv)

    current_stage = SeasonSettings.objects.first().curr_stage
    if (current_stage != 'pre' and current_stage != 'init_tourn'):

        current_stage = SeasonSettings.objects.first().curr_stage

        df = get_curr_player_df()

        update_cut_players(df)

        for team in Team.objects.all():
            team_name = team.team_name
            team_cut = check_cut(team_name, df)
            curr_team_pts = get_team_score(team_name, df)
            team.cut = team_cut
            team.team_points = curr_team_pts
            team.save()

        # Set Round Values used in HTML Bools
        r1_bool = False
        r2_bool = False
        r3_bool = False
        r4_bool = False

        if (current_stage == 'r_1'):
            r1_bool = True

        elif (current_stage == 'r_2'):
            r2_bool = True

        elif (current_stage == 'r_3'):
            r3_bool = True

        elif (current_stage == 'r_4'):
            r4_bool = True

        teams = Team.objects.filter(cut = False)
        
        cut_teams = Team.objects.filter(cut = True)

        teams_list = {
            'teams': teams,
            'cut_teams' : cut_teams,
            'r1' : r1_bool,
            'r2' : r2_bool,
            'r3' : r3_bool,
            'r4' : r4_bool,
            'pre_tour': False,
        }

        return render(request, 'golf_app/standings.html', teams_list)

    elif (current_stage == 'init_tourn' and Golfer.objects.count() < 10):

        curr_df = get_curr_player_csv()
        initalize_players(curr_df )
        update_player_prices()
        pre_tour = True
        return render(request, 'golf_app/standings.html', {'pre_tourn': pre_tour})

    else:
        pre_tour = True
        return render(request, 'golf_app/standings.html', {'pre_tourn': pre_tour})

def inttocommas(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))