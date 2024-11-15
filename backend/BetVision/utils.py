import requests

# API Keys
ODDS_API_KEY = "b9922d167979d126cb48be9726f8d66f"
SPORTSDATAIO_API_KEY = "25a2492d13894327a60e4b8acd6ffb90"

# Fetch team stats from SportsData.io
def fetch_team_data(league):
    """
    Fetch team stats from SportsData.io.
    """
    API_URL = f"https://api.sportsdata.io/v3/nba/scores/json/AllTeams?key=25a2492d13894327a60e4b8acd6ffb90"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
def fetch_top_nba_teams(num_teams, season="2024"):
    """
    Fetch NBA team standings from SportsData.io and return the top teams based on win percentage.
    """
    API_URL = f"https://api.sportsdata.io/v3/nba/scores/json/Standings/{season}?key={SPORTSDATAIO_API_KEY}"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        standings_data = response.json()

        # Sort teams by win percentage in descending order
        sorted_teams = sorted(standings_data, key=lambda team: team.get('WinPercentage', 0), reverse=True)

        # Return the top N teams based on win percentage
        return sorted_teams[:num_teams]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching NBA standings data: {e}")
        return None


# Fetch live moneyline odds from the Odds API

def fetch_live_moneyline_odds(team_names):
    """
    Fetch live moneyline odds from The Odds API using the provided URL.
    """
    API_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/"
    params = {
        "apiKey": "b9922d167979d126cb48be9726f8d66f",
        "regions": "us",      # Specify region, e.g., 'us' for U.S. odds
        "markets": "h2h",     # Market type, e.g., 'h2h' for moneyline odds
        "oddsFormat": "decimal"
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        odds_data = response.json()

        # Filter odds data to include only games involving any of the specified teams
        relevant_odds = [
            game for game in odds_data
            if any(team_name in game.get('home_team', '') or team_name in game.get('away_team', '') for team_name in team_names)
        ]

        return relevant_odds

    except requests.exceptions.RequestException as e:
        print(f"Error fetching odds data: {e}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching odds data: {e}")
        return None

# Generate moneyline parlays
def generate_moneyline_parlay_suggestions(preferences):
    """
    Generate moneyline parlay suggestions using fetched odds.
    """
    legs = preferences.get('legs', 3)
    league = preferences.get('league', 'nba')

    # Fetch odds
    odds = fetch_live_moneyline_odds(league)
    print("DEBUG: Odds fetched:", odds)  # Debugging line

    # Validate odds
    if not odds or not isinstance(odds, list):
        return [{"error": "Invalid odds format or no odds available"}]

    # Generate suggestions
    parlay_suggestions = []
    teams_list = odds[:legs]  # Slicing top 'legs' items

    for team in teams_list:
        parlay_suggestions.append({
            "team": team.get('home_team', 'Unknown'),  # Handle missing keys
            "moneyline_odds": team.get('bookmakers', [{}])[0].get('markets', [{}])[0].get('outcomes', [{}])[0].get('price', 'N/A'),
            "payout": "$200",  # Mock payout
            "probability": "50%"  # Mock probability
        })

    return parlay_suggestions
