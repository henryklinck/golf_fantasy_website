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

    str_df = df.to_string()

    print(str_df)

    return 

#def update_players(Dataframe curr_df):
