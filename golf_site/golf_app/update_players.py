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

    for index, row in curr_df.iterrows():

        if (round == 'R1'):
            curr_points = row[round]
            course_par = SeasonSettings.objects.first().course_par

            if (curr_points == '-'):
                Golfer.objects.update_or_create(
                    # Check if value is a number or a dash - Rep dash as 200 points / Player has not Started
                    # row['PLAYER'] refers to player name
                    point = row['PLAYER'],
                )
    
            else:
                Golfer.objects.update_or_create(
                    # Check if value is a number or a dash - Rep dash as 200 points / Player has not Started
                    # row['PLAYER'] refers to player name
                    point = curr_points - course_par,
                )

        elif (round == 'R2'):
            curr_points = row[round]

        elif (round == 'R3'):
            curr_points = row[round]

        elif (round == 'R4'):
            curr_points = row[round]

        

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
                player_cost = 100
            )
    
    # Update Player Values from Tourn Info Csv
    # tourn_csv_file = csv.reader(open('./tourn_info.csv', "r"), delimiter=",")

    #for row in tourn_csv_file:
    #if current rows 2nd value is equal to input, print that row
        #if number == row[1]:
    #    print (row)


def check_cut(name):
    team = Team.objects.filter(team_name = name)
    if (team.cut):
        return
    else:
        num_non_cut_golfers = 0
        for golfer in team:
            if not (golfer.cut):
                num_non_cut_golfers += 1

        if (num_non_cut_golfers < 4):
            team.cut = True