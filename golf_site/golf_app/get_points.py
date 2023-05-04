from django import forms
from .models import Team, Golfer, SeasonSettings
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import requests
import csv

def get_curr_player_df():
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

def update_cut_players(df):
    # If player is cut, set Golder.cut = True
    course_par = SeasonSettings.objects.first().course_par

    for index, row in df.iterrows():
        if (row['POS'] == 'CUT' or row['POS'] == 'WD' or row['POS'] == 'DQ'):
            name = row['PLAYER']
            golfer = Golfer.objects.get(name = name)
            golfer.cut = True
            golfer.save()


def check_cut(name, df):
    team = Team.objects.get(team_name = name)
    if (team.cut):
        return True
    else:
        num_non_cut_golfers = 0
        for golfer in team.team_golfers.all():
            if not (golfer.cut):
                num_non_cut_golfers += 1

        if (num_non_cut_golfers < 4):
            return True
        return False

def get_team_score(team_name, df):
    # Return team score
    # Different Processes in Each Round
    curr_round = SeasonSettings.objects.first().curr_stage
    team = Team.objects.get(team_name = team_name)
    team_golfers = team.team_golfers.all()

    if (curr_round == 'r_1'):
        # Current Round: Round One
        golfer_scores = []
        for golfer in team_golfers:
            name = golfer.name
            for index, row in df.iterrows():
                if (name == row['PLAYER'] and row['R1'] != '-' and not golfer.cut):
                    golfer_scores.append(int(row['TOT']))
                elif (name == row['PLAYER'] and row['R1'] == '-' and not golfer.cut):
                    # Player not out yet
                    golfer_scores.append(0)
        golfer_scores.sort()

        team_score = sum(golfer_scores[0:4])

        return team_score

    elif (curr_round == 'r_2'):
        # Current Round: Round Two
        # Determine Round 1 Points
        # Determine Round 2 Points
        par = SeasonSettings.objects.first().course_par
        round_1_scores = []
        golfer_scores = []
        for golfer in team_golfers:
            name = golfer.name
            for index, row in df.iterrows():
                if (name == row['PLAYER']):
                    # Add R1 Values
                    if ((row['R1']) != '-'):
                        r1_score = int(row['R1']) - par
                        round_1_scores.append(r1_score)

                if (name == row['PLAYER'] and row['R2'] != '-' and not golfer.cut):

                    # Next 4 Lines Adds R2 Values
                    tot_score = int(row['TOT']) - r1_score
                    golfer_scores.append(tot_score)
                elif (name == row['PLAYER'] and row['R2'] == '-' and not golfer.cut):

                    golfer_scores.append(0)

        # round_1_scores contains top 4 from round 2
        round_1_scores.sort()
        team_score = sum(round_1_scores[0:4])

        # golfer_scores contains top 4 from round 2
        golfer_scores.sort()

        team_score = team_score + sum(golfer_scores[0:4])

        return team_score

    elif (curr_round == 'r_3'):
        # Current Round: Round Three
        # Determine Round 1, 2, 3 Points

        par = SeasonSettings.objects.first().course_par
        round_1_scores = []
        round_2_scores = []
        golfer_scores = []
        for golfer in team_golfers:
            name = golfer.name
            for index, row in df.iterrows():
                if (name == row['PLAYER']):
                    # Add R1 Values
                    if ((row['R1']) != '-'):
                        r1_score = int(row['R1']) - par
                        round_1_scores.append(r1_score)

                    # Add R2 Values
                    if ((row['R2']) != '-'):
                        r2_score = int(row['R2']) - par
                        round_2_scores.append(r2_score)

                if (name == row['PLAYER'] and row['R3'] != '-' and not golfer.cut):

                    # Next 4 Lines Adds Earlier Values
                    tot_score = int(row['TOT']) - r1_score - r2_score
                    golfer_scores.append(tot_score)

                elif (name == row['PLAYER'] and row['R3'] == '-' and not golfer.cut):

                    golfer_scores.append(0)
                    
        # round_1_scores contains top 4 from round 2
        round_1_scores.sort()
        team_score = sum(round_1_scores[0:4])

        # round_2_scores contains top 4 from round 2
        round_2_scores.sort()
        team_score = team_score + sum(round_2_scores[0:4])

        # golfer_scores contains top 4 from round 2
        golfer_scores.sort()
        team_score = team_score + sum(golfer_scores[0:4])

        return team_score

    elif (curr_round == 'r_4'):
        # Current Round: Round Three
        # Determine Round 1, 2, 3, 4 Points

        par = SeasonSettings.objects.first().course_par
        round_1_scores = []
        round_2_scores = []
        round_3_scores = []
        golfer_scores = []
        for golfer in team_golfers:
            name = golfer.name
            for index, row in df.iterrows():
                if (name == row['PLAYER']):
                    # Add R1 Values
                    if ((row['R1']) != '-'):
                        r1_score = int(row['R1']) - par
                        round_1_scores.append(r1_score)

                    # Add R2 Values
                    if ((row['R2']) != '-'):
                        r2_score = int(row['R2']) - par
                        round_2_scores.append(r2_score)

                    # Add R3 Values
                    if ((row['R3']) != '-'):
                        r3_score = int(row['R3']) - par
                        round_3_scores.append(r3_score)

                if (name == row['PLAYER'] and row['R4'] != '-' and not golfer.cut):
                    
                    # Next 4 Lines Adds Earlier Values
                    tot_score = int(row['TOT']) - r1_score - r2_score - r3_score
                    golfer_scores.append(tot_score)

                elif (name == row['PLAYER'] and row['R4'] == '-' and not golfer.cut):

                    golfer_scores.append(0)
                    
        # round_1_scores contains top 4 from round 2
        round_1_scores.sort()
        team_score = sum(round_1_scores[0:4])

        # round_2_scores contains top 4 from round 2
        round_2_scores.sort()
        team_score = team_score + sum(round_2_scores[0:4])

        # round_3_scores contains top 4 from round 2
        round_3_scores.sort()
        team_score = team_score + sum(round_3_scores[0:4])

        # golfer_scores contains top 4 from round 2
        golfer_scores.sort()

        team_score = team_score + sum(golfer_scores[0:4])

        return team_score
    return 0