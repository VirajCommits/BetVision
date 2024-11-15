from django.urls import path
from . import views

urlpatterns = [
    path('fetch-teams/', views.fetch_teams, name='fetch_teams'),
    path('generate-moneyline-suggestions/', views.generate_moneyline_suggestions, name='generate_moneyline_suggestions'),
    path('fetch-live-odds/', views.fetch_live_odds, name='fetch_live_odds'),
]
