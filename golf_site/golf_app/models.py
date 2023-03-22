from django.db import models
from datetime import datetime

class SeasonSettings(models.Model):
    team_budget = models.IntegerField()
    team_size = models.IntegerField()
    user_password = models.CharField(max_length=30)
    course_par = models.IntegerField(default=0)
    tourn_pga_link = models.CharField(max_length=100, default="a")

# models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    timestamp = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title


class Golfer(models.Model):
    player_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=15)
    player_cost = models.IntegerField()
    cut = models.BooleanField(default=False)
    point = models.IntegerField()

    def __str__(self):
        return self.name + " ($" + str(self.player_cost) + ")"

    @classmethod
    def create_update(name, player_cost, cut, point):
        Golfer.objects.create(name= name, player_cost = player_cost, cut = cut ,point = point)
        


class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_owner = models.CharField(max_length=30, unique=True)
    team_cost = models.IntegerField(default=0)
    # team_golfers = feighn key / many to many https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
    team_golfers = models.ManyToManyField(Golfer)
    team_points = models.IntegerField(default=0)
    creation_time = models.DateTimeField(default=datetime.now)
    password_used = models.CharField(default="test", max_length=30)

    def __str__(self):
        return self.team_name


