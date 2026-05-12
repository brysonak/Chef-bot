import steamleaderboardsWill as steamboards
import requests
import os

# -- helper classes
class LeaderboardInfo:
    def __init__(self, _steamid, _pretty_name):
        self.steamid = _steamid
        self.pretty_name = _pretty_name

# -- constants
ORG_API_KEY = os.getenv("ORG_API_KEY")
print(f'BytebackStudios org API key parsed from env: {ORG_API_KEY}')

NMK_APP_ID = 3077140
NMK_PLAYTEST_APP_ID = 3471110
NMK_LEADERBOARD_MAP = {
    'flappy' : LeaderboardInfo('leaderboard_nmk_flappy', 'Flappy'),
    'stack' : LeaderboardInfo('leaderboard_nmk_stack', 'Stack'),
    'rope' : LeaderboardInfo('leaderboard_nmk_rope', 'Rope')
}

def get_supported_boards():
    return list(NMK_LEADERBOARD_MAP)

def print_supported_boards():
    print('The following leaderboards are supported and can be queried: ')
    for key in NMK_LEADERBOARD_MAP:
        print(f"\t{key}")

def print_score(entry):
    print(str(entry))

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

def get_board(boardid):
    board_data = NMK_LEADERBOARD_MAP[boardid]
    nmk_leaderboards = steamboards.LeaderboardGroup(NMK_PLAYTEST_APP_ID)
    leaderboard = nmk_leaderboards.get(name=board_data.steamid)
    
    return leaderboard

def query_board_top(boardid, top_count=10):
    leaderboard = get_board(boardid)
    all_scores = leaderboard.entries

    top_board = []

    idx = 0
    for entry in all_scores:
        if entry == None:
            print(f'No score exists in leaderboard {boardid} at rank {idx + 1}')
            continue

        entry.SetPersona(steamid_to_username(entry.steam_id))
        top_board.append(entry)
        idx += 1
        if idx > top_count:
            break
    
    return top_board

def query_board_user(boardid, userid):
    leaderboard = get_board(boardid)
    my_score = leaderboard.find_entry(userid)

    if my_score == None:
        print(f'No score exists in leaderboard {boardid} for Steam userid {userid}')
    else:
        my_score.SetPersona(steamid_to_username(my_score.steam_id))
        print_score(my_score)

def query_board_rank(boardid, rank=1):
    leaderboard = get_board(boardid)
    rank_score = leaderboard.find_entry(rank=1)

    if rank_score == None:
        print(f'No score exists in leaderboard {boardid} at rank {rank}')
    else:
        rank_score.SetPersona(steamid_to_username(rank_score.steam_id))
        print_score(rank_score)

# -- example: query top 10 scores in flappy game
#query_board_top('flappy')

# -- example: query a user's score in stack game using their steamid
#query_board_user(501623985670965)

# -- example: query the #3 score in all arcade games
#for key in NMK_LEADERBOARD_MAP:
#   query_board_rank(key, 3)