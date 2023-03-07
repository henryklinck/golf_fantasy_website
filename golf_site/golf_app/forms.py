from django.forms import ModelForm
from django import forms
from .models import Team, Golfer

class TeamForm(ModelForm):
    team_name = forms.CharField(max_length=30)
    team_owner = forms.CharField(max_length=30)
    #team_cost = forms.IntegerField()
    team_golfers = forms.ModelMultipleChoiceField(
        queryset=Golfer.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    password_used = forms.CharField(max_length=30)
    #team_points = forms.IntegerField()
    class Meta:
        model = Team
        fields = ['team_name','team_owner', 'team_golfers', 'password_used']
