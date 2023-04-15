from django.forms import ModelForm
from django import forms
from .models import Team, Golfer, SeasonSettings
from django.utils.safestring import mark_safe

class TeamForm(ModelForm):
    team_name = forms.CharField(max_length=30, label=mark_safe('<br /> Team Name:')) 
    team_owner = forms.CharField(max_length=30, label=mark_safe('<br /> Email'))
    password_used = forms.CharField(max_length=30, label=mark_safe('<br /> Password'))
    #team_cost = forms.IntegerField()
    team_golfers = forms.ModelMultipleChoiceField(
        queryset=Golfer.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'golfers_list'}),
        label=mark_safe('<br /><br /> <b> Minimum 4 - Maximum - 7<b><br>Select Your Players Below')
    )
    #team_points = forms.IntegerField()
    class Meta:
        model = Team
        fields = ['team_name','team_owner', 'password_used', 'team_golfers']

class ConfmForm(ModelForm):
    team_name = forms.CharField(max_length=30) 
    team_owner = forms.CharField(max_length=30)
    team_cost = forms.IntegerField()
    team_golfers = forms.ModelMultipleChoiceField(
        queryset=Golfer.objects.all().order_by('name')
    )

    class Meta:
        model = Team
        fields = ['team_name','team_owner', 'team_cost', 'team_golfers']

