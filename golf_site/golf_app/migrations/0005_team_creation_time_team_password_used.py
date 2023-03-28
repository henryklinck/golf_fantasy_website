# Generated by Django 4.1.5 on 2023-03-05 04:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0004_seasonsettings_alter_team_team_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='team',
            name='password_used',
            field=models.CharField(default='test', max_length=30),
        ),
    ]