from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .utils import fetch_team_data, generate_moneyline_parlay_suggestions, fetch_live_moneyline_odds, fetch_top_nba_teams
from rest_framework.permissions import IsAuthenticated
# Create your views here.


@api_view(['GET'])
def fetch_teams(request):
    """
    Fetch team stats using SportsData.io.
    """
    league = request.GET.get('league', 'nba')  # Default to NBA
    data = fetch_team_data(league)
    return JsonResponse({'success': True, 'teams': data})

@api_view(['POST'])
def generate_moneyline_suggestions(request):
    """
    Generate moneyline parlay suggestions.
    """
    num_parlays = request.data.get('num_parlays')

    # Fetch the top NBA teams based on standings
    top_teams = fetch_top_nba_teams(num_parlays)
    if not top_teams:
        return JsonResponse({"success": False, "error": "Failed to fetch NBA team standings data"})

    # Extract team names for odds fetching
    team_names = [team['Name'] for team in top_teams]

    # Fetch odds for games involving the top teams
    odds = fetch_live_moneyline_odds(team_names)
    if not odds:
        return JsonResponse({"success": False, "error": "No odds data available for the selected teams"})

    # Create predictions based on odds data and top team standings
    predictions = []
    for game in odds:
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        predictions.append({
            "teams": f"{home_team} vs {away_team}",
            "moneyline_odds": {
                "home_team": game.get('bookmakers', [{}])[0].get('markets', [{}])[0].get('outcomes', [{}])[0].get('price', 'N/A'),
                "away_team": game.get('bookmakers', [{}])[0].get('markets', [{}])[0].get('outcomes', [{}])[1].get('price', 'N/A')
            }
        })

    return JsonResponse({"success": True, "predictions": predictions})

@api_view(['GET'])
def fetch_live_odds(request):
    """
    Fetch live moneyline odds using Odds API.
    """
    league = request.GET.get('league', 'nba')  # Default to NBA
    odds = fetch_live_moneyline_odds(league)
    return JsonResponse({'success': True, 'odds': odds})