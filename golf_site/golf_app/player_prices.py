
from .models import Golfer
import csv

from django.conf import settings


def update_player_prices():
    value = settings.BASE_DIR
    csv_path = value / 'golf_app/tourn_info.csv'

    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            name1 = str(row[0])
            name1 = name1.split(' ')
            formatted_name = name1[0][0] + ". " + name1[1]
            
            for golfer in Golfer.objects.all():
                golfer_name = golfer.name.split()
                
                golfer_formatted_name = golfer_name[0][0] + ". " + golfer_name[1]

                if (golfer_formatted_name == formatted_name):
                    golfer.player_cost = int(row[1])
                    golfer.save()
            
        print(f'Processed {line_count} lines.')
    return 0
    