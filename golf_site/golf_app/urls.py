from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('build_team/', views.build_team, name='build_team'),
    path('standings/', views.standings, name='standings'),
    path('confm_team/', views.confm_team, name='confm_team')
]