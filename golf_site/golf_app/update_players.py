from django import forms
from .models import Team, Golfer, SeasonSettings
from bs4 import BeautifulSoup
import json
import pandas as pd
import requests
import csv

def get_curr_player_csv():
    url = SeasonSettings.objects.first().tourn_pga_link

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    data = json.loads(soup.find(id='leaderboard-seo-data').text)

    all_data = data['mainEntity']['csvw:tableSchema']['csvw:columns']

    accum = {}
    for column in all_data:
        title = column['csvw:name']
        accum[title] = list((pd.Series(column['csvw:cells']).apply(pd.Series))['csvw:value'])
    
    df = pd.DataFrame(accum)

    return df

def updates_players(curr_df, round):
    ''' 
    Argument Dataframe contains current golfer information at given tournament 
    '''
    #str_df = curr_df.to_string()

    # Current Round is Represented by Arg: round
    print(curr_df.to_string())

    course_par = SeasonSettings.objects.first().course_par

    for index, row in curr_df.iterrows():
        
        if not (row['POS'] == 'CUT' or row['POS'] == 'WD' or row['POS'] == 'DQ'):

            # row['PLAYER'] refers to player name
            # if Position not Cut

            if (round == 'R1'):
                curr_points = row[round]
                

                if (curr_points == '-'):
                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = False
                    )
        
                else:
                    gname = row['PLAYER']

                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = True,
                        r1_points = int(curr_points) - course_par,
                        point = int(curr_points) - course_par
                        )
                    #print(Golfer.objects.filter(name=gname).r1_points)

            elif (round == 'R2'):
                curr_points = row[round]
                if (curr_points == '-'):
                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = False
                    )
        
                else:
                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = True,
                        r2_points = int(curr_points) - course_par,
                        point = (int(curr_points) - course_par) + Golfer.objects.filter(name=row['PLAYER']).first().r1_points
                    )


            elif (round == 'R3'):
                curr_points = row[round]
                if (curr_points == '-'):
                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = False
                    )
        
                else:
                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = True,
                        r3_points = int(curr_points) - course_par,
                        point = (int(curr_points) - course_par) + Golfer.objects.filter(name=row['PLAYER']).first().r1_points +
                        Golfer.objects.filter(name=row['PLAYER']).first().r2_points
                    )

            elif (round == 'R4'):
                curr_points = row[round]
                if (curr_points == '-'):
                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = False
                    )
        
                else:
                    Golfer.objects.filter(name = row['PLAYER']).update(
                        started_round = True,
                        r4_points = int(curr_points) - course_par,
                        point = (int(curr_points)- course_par) + Golfer.objects.filter(name=row['PLAYER']).first().r1_points +
                        Golfer.objects.filter(name=row['PLAYER']).first().r2_points +
                        Golfer.objects.filter(name=row['PLAYER']).first().r3_points
                    )
        
        else:
            Golfer.objects.filter(name=row['PLAYER']).update(
                cut = True
            )

    return
        

def initalize_players(curr_df):
    ''' 
    Argument Dataframe contains current golfer information at given tournament 
    '''
    str_df = curr_df.to_string()

    print(str_df)

    # Find Most Recent Round

    for index, row in curr_df.iterrows():
        Golfer.objects.update_or_create(
                # row['PLAYER'] refers to player name
                name = row['PLAYER'],
                player_cost = 0
            )
    
    # Update Player Values from Tourn Info Csv
    # tourn_csv_file = csv.reader(open('./tourn_info.csv', "r"), delimiter=",")

    #for row in tourn_csv_file:
    #if current rows 2nd value is equal to input, print that row
        #if number == row[1]:
    #    print (row)


#def get_top_4_golfers(team_name, )


def check_cut(name):
    team = Team.objects.filter(team_name = name).first()
    if (team.cut):
        return
    else:
        num_non_cut_golfers = 0
        for golfer in team.team_golfers.all():
            if not (golfer.cut):
                num_non_cut_golfers += 1

        if (num_non_cut_golfers < 4):
            team.cut = True
            team.save()