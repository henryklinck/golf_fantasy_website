from django.db import models

class SeasonSettings(models.Model):
    team_budget = models.IntegerField()
    team_size = models.IntegerField()
    user_password = models.CharField(max_length=30)
    course_par = models.IntegerField(default=0)
    tourn_pga_link = models.CharField(max_length=100, default="a")
    STAGES = {
        ('pre', 'Pre Tournament'),
        ('r_1', 'Round 1'),
        ('r_2', 'Round 2'),
        ('r_3', 'Round 3'),
        ('r_4', 'Round 4')
    }
    curr_stage = models.CharField(
        max_length=30,
        choices=STAGES,
        default='pre',
    )

# models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    timestamp = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title


class Golfer(models.Model):
    #player_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=15)
    player_cost = models.IntegerField()
    cut = models.BooleanField(default=False)
    r1_points = models.IntegerField(default=0)
    r2_points = models.IntegerField(default=0)
    r3_points = models.IntegerField(default=0)
    r4_points = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " ($" + str(self.player_cost) + ")"

    @classmethod
    def create_update(name, player_cost, cut, point):
        Golfer.objects.create(name= name, player_cost = player_cost, cut = cut ,point = point)
        


class Team(models.Model):
    team_name = models.CharField(max_length=30, unique=True)
    team_owner = models.CharField(max_length=30)
    team_cost = models.IntegerField(default=0)
    # team_golfers = feighn key / many to many https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
    team_golfers = models.ManyToManyField(Golfer)
    team_points = models.IntegerField(default=0)
    #creation_time = models.DateTimeField(timezone.now())
    password_used = models.CharField(default="test", max_length=30)
    r_1_points = models.IntegerField(default=0)
    r_2_points = models.IntegerField(default=0)
    r_3_points = models.IntegerField(default=0)
    r_4_points = models.IntegerField(default=0)
    cut = models.BooleanField(default=False)

    def __str__(self):
        return self.team_name


