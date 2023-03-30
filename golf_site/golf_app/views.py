# from django.http import HttpResponse
#from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import TeamForm, ConfmForm
from django.contrib import messages
from .update_players import get_curr_player_csv, updates_players, check_cut
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
    
    # Submit Team is Clicked
    if request.method=='POST' and 'btnform1' in request.POST:
        print('TEST')
        team_form = TeamForm(request.POST)
        print(str(team_form.is_valid()))
        print(team_form.instance.password_used)
        if team_form.is_valid():
            password = team_form.cleaned_data['password_used']

            # Check if Entered Password is Correct
            if (password == SeasonSettings.objects.first().user_password):

                name = team_form.cleaned_data['team_name']
                owner = team_form.cleaned_data['team_owner']
                golfers = team_form.cleaned_data['team_golfers']

                for golfer in golfers:
                    print(golfer.name)

                curr_spent = 0
                team_players = set()
                for golfer in golfers:
                    curr_spent += golfer.player_cost
                    team_players.add(golfer.name)
                
                # Check if Team Cost > Max Budget
                if (curr_spent > int(SeasonSettings.objects.first().team_budget)):
                    messages.info(request, 'This Team Value Surpasses Max Budget')
                    
                    # Load Page With Current Form Inputs
                    form2 = Team.objects.get(team_name=name)  
                    form1 = TeamForm(instance=form2)

                    Team.objects.get(team_name=team_form.instance.team_name).delete()

                    max_budget = str(SeasonSettings.objects.first().team_budget) 
                    return render(request, 'golf_app/build_team.html', {'team_form': form1,
                                                                'max_budget': max_budget,})
    

                temp_team = Team.objects.create(team_name=name, team_owner=owner, team_cost=curr_spent)

                for golfer in golfers:
                    temp_team.team_golfers.add(golfer)

                form2 = Team.objects.get(team_name=name)  
                conf_form = ConfmForm(instance=form2)

                Team.objects.get(team_name=name).delete()

                print("TEST!3")
                return render(request, 'golf_app/confm_team.html', 
                    {
                    'confm_form': conf_form, 
                    'confm_name': name,
                    'confm_owner': owner,
                    'confm_team_cost': str(curr_spent),
                    'confm_golfers': team_players,
                    'false' : False
                    })

            else:
                # Wrong Password Entered
                messages.info(request, 'Your password is incorrect')

    # Calculate Cost Button is Clicked
    elif request.method=='POST' and 'btnform2' in request.POST:
        print("TEST YO")
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            total_cost = 0
            team_form.save()
            curr_team = Team.objects.get(team_name=team_form.instance.team_name)

            total_cost = 0
            for golfer in curr_team.team_golfers.all():
                total_cost += golfer.player_cost
            
            # Print Total Cost
            if total_cost > SeasonSettings.objects.first().team_budget:
                messages.info(request, 'Over Budget - Total Cost is $' + str(total_cost))
            else:
                messages.info(request, 'Under Budget - Total Cost is $' + str(total_cost))

            # Load Page With Current Form Inputs
            team_name1 = team_form.instance.team_name
            form2 = Team.objects.get(team_name=team_name1)  
            form1 = TeamForm(instance=form2)

            Team.objects.get(team_name=team_form.instance.team_name).delete()

            max_budget = str(SeasonSettings.objects.first().team_budget) 
            return render(request, 'golf_app/build_team.html', {'team_form': form1,
                                                        'max_budget': max_budget,})

    # If No Clicks, Load Empty Page
    max_budget = str(SeasonSettings.objects.first().team_budget) 
    return render(request, 'golf_app/build_team.html', {'team_form': TeamForm(),
                                                        'max_budget': max_budget,})


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
    current_stage = SeasonSettings.objects.first().curr_stage
    if (current_stage != 'pre' and current_stage != 'init_tourn'):

        current_stage = SeasonSettings.objects.first().curr_stage

        points_df = get_curr_player_csv()

        if (current_stage == 'r_1'):
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


        for team in Team.objects.all():
            # Get Team's Current Points
            # Check if Team is Cut
            num_non_cut_golfers = 0
            team_pts_so_far = 0

            # Add Team's Point's In Current Round + Add Round Points to Make Total Points
            if not (team.cut):
                for golfer in team.team_golfers.all():
                    if not (golfer.cut):
                        num_non_cut_golfers += 1

                        if (current_stage == 'r_1'):
                            team_pts_so_far += golfer.r1_points
                        elif (current_stage == 'r_2'):
                            team_pts_so_far += golfer.r2_points
                        elif (current_stage == 'r_3'):
                            team_pts_so_far += golfer.r3_points
                        elif (current_stage == 'r_4'):
                            team_pts_so_far += golfer.r4_points
            
            if (current_stage == 'r_1'):
                team.r_1_points = team_pts_so_far
                team.team_points = team_pts_so_far
            elif (current_stage == 'r_2'):
                team.r_2_points = team_pts_so_far
                team.team_points = team.r_1_points + team_pts_so_far
            elif (current_stage == 'r_3'):
                team.r_3_points = team_pts_so_far
                team.team_points = team.r_1_points + team.r_2_points + team_pts_so_far
            elif (current_stage == 'r_4'):
                team.r_4_points = team_pts_so_far
                team.team_points = team.r_1_points + team.r_2_points + team.r_3_points + team_pts_so_far

            if (num_non_cut_golfers < 4):
                team.cut = True

            team.save()

        teams = Team.objects.filter(cut=False).order_by('team_points')
        cut_teams = Team.objects.filter(cut=True).order_by('team_points')

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

        teams_list = {
            'teams': teams,
            'cut_teams' : cut_teams,
            'r1' : r1_bool,
            'r2' : r2_bool,
            'r3' : r3_bool,
            'r4' : r4_bool,
        }

        return render(request, 'golf_app/standings.html', teams_list)

    elif (current_stage == 'init_tourn' and Golfer.objects.count() < 10):

        curr_df = get_curr_player_csv()
        initalize_players(curr_df )
        return render(request, 'golf_app/standings.html', {})

    else:
        return render(request, 'golf_app/standings.html', {})