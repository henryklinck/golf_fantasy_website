from django.forms import ModelForm
from django import forms
from .models import Team, Golfer
#
class TeamForm(ModelForm):
    team_name = forms.CharField(max_length=30)
    team_owner = forms.CharField(max_length=30)
    team_cost = forms.IntegerField()
#    # team_golfers = feighn key / many to many https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
    team_golfers = forms.ModelMultipleChoiceField(
        queryset=Golfer.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    team_points = forms.IntegerField()
    class Meta:
        model = Team
        fields = ['team_name','team_owner', 'team_cost', 'team_golfers','team_points']