# Generated by Django 4.1.5 on 2023-03-28 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf_app', '0012_alter_team_creation_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='creation_time',
        ),
    ]