# Generated by Django 4.1.5 on 2023-03-28 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0010_remove_golfer_player_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creation_time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 3, 28, 23, 5, 56, 250993, tzinfo=datetime.timezone.utc)),
        ),
    ]
