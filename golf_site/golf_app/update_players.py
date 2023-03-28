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

    # str_df = df.to_string()

    #print(str_df)

    return df

def updates_players(curr_df):
    ''' 
    Argument Dataframe contains current golfer information at given tournament 
    '''
    #str_df = curr_df.to_string()

    # Find Most Recent Round

    for index, row in curr_df.iterrows():

        # Ckeck if player is CUT
        if (row['POS'] == "CUT"):
            Golfer.objects.update_or_create(
                # row['PLAYER'] refers to player name
                name = row['PLAYER'],
                player_cost = 110,
                cut = True,
                point = row['R1']
            )
        else:
            Golfer.objects.update_or_create(
                name = row['PLAYER'],
                player_cost = 100,
                point = row['R1']
            )

    #print(str_df)

    #curr_csv = curr_df.to_csv()

    #print(type(curr_csv))

    #recent_round_index = 0

    #with open(curr_csv, 'r') as csvfile:
    #    reader = csv.reader(csvfile)
    #    for row in reader:
    #        #print(row[2])

#def update_players(Dataframe curr_df):
