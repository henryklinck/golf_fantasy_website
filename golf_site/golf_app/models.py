from django.db import models

# Fantasy Settings
# Team Budget
# Team size
# Website Password

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    timestamp = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title


class Golfer(models.Model):
    player_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    player_cost = models.IntegerField()
    point = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name + " ($" + str(self.player_cost) + ")"


class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_owner = models.CharField(max_length=30, unique=True)
    team_cost = models.IntegerField()
    # team_golfers = feighn key / many to many https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
    team_golfers = models.ManyToManyField(Golfer)
    team_points = models.IntegerField()

    def __str__(self):
        return self.team_name


