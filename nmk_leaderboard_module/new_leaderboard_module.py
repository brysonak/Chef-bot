import os
import requests

ORG_API_KEY = os.getenv("ORG_API_KEY")
print(f'BytebackStudios org API key parsed from env: {ORG_API_KEY}')
APP_ID = 5205560
LEADERBOARD_IDS = {"flappy": 20813946, "stack":20813949, "rope":20813947, "ddr":20813945}

url = "https://partner.steam-api.com/ISteamLeaderboards/GetLeaderboardEntries/v1/"

def getLeaderboards(id):
    params = {
        "key": ORG_API_KEY,
        "appid": 5205560,
        "leaderboardid": LEADERBOARD_IDS[id],       # Must be the numeric ID, not the string name!
        "datarequest": "RequestGlobal",# Enforce string representation 
        "rangestart": 1,               # Changed from start -> rangestart
        "rangeend": 10,                # Changed from end -> rangeend
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    #print(f"HTTP Status Code: {response.status_code}")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        print(f"Raw Server Response:\n{response.text}")
        return None
    return response.json()

def steamid_to_username(steamid):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={ORG_API_KEY}&steamids={steamid}"
    
    try:
        response = requests.get(url)
        data = response.json()

        # Dig into the JSON structure to find the personaname
        players = data.get("response", {}).get("players", [])
        if players:
            return players[0].get("personaname")
        else:
            return "User not found or profile is private."
            
    except Exception as e:
        return f"Error: {str(e)}"

def extract_leaderboard_data(board):
  json_data = getLeaderboards(board)
  entries = json_data.get('leaderboardEntryInformation', {}).get(
      'leaderboardEntries', []
  )
  return [
      {
          'persona': steamid_to_username(entry.get('steamID')),
          'rank': entry.get('rank'),
          'score': entry.get('score'),
      }
      for entry in entries
  ]

def format_leaderboard_data(board):
    data = extract_leaderboard_data(board)
    string = ""
    for item in data:
        string += f"Rank:{item["rank"]}, Score: {item["score"]}, User: {item["persona"]} \n"
    return string

