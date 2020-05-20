from datetime import datetime, timedelta
from json import dump, load, loads
from pathlib import Path
from requests import get


""" TO DO """
# 1. Trophy reset
# 2. Power play reset
# 3. Bonus box extra progression (based on time and assumed quest completions)
# 4. How much money would be required to max account, using 80 gem mega boxes
#      Might have to save brawler rarities somewhere, and legendary drop rates
# 5. Which season (number) to max out, with and without brawl pass (requires #3)
#      Have to take into account the progression of the new guaranteed brawler?
# 6. Progression since last update (in dollars)


""" GAME CONSTANTS """
#         0  1   2   3   4    5    6    7    8     9  10
POINTS = [0, 20, 30, 50, 80,  130, 210, 340, 550,  0, 0]
COINS = [00, 20, 35, 75, 140, 290, 480, 800, 1250, 0, 0]
""" GAME VARIABLES """
CURRENT_SEASON = 1
SEASON_1_END = datetime(2020, 7, 6, 4)
SEASON_RESET_EPOCH = datetime(2020, 5, 4, 4)
POWER_PLAY_EPOCH = datetime(2020, 5, 11, 22)
""" PROGRESSION VALUES """
BRAWL_BOX = 53.7


# ========== Data from server ==================================================
def apirequest(apitail):
    """
    Pulls the API request from the server.
    apitail must be a valid url tail.
    """
    # Open API token
    with open('BrawlStars/token.txt') as tokenfile:
        headers = {
            'Accept': 'application/json',
            'authorization': f'Bearer {tokenfile.read()}'
        }
    # Query server
    response = get(f'https://api.brawlstars.com/v1/{apitail}', headers=headers)
    if response.status_code == 200:
        return loads(response.content.decode('utf-8'))
    else:
        print(f"Error code: {response.status_code}")
        return None


def get_playerdata(playertag):
    return apirequest(f"players/%23{playertag}")


# ========== Print formatting ==================================================
def print_time_remaining(seasontype, seasonnum=0, seasonname="<empty>"):
    """
    Prints the time remaining until the season ends.
    Seasontype is one of "brawl pass", "trophies", "power play"
    """
    if seasontype == "brawl pass":
        remaining = SEASON_1_END - datetime.now()
        printstr = f"Season {seasonnum}: {seasonname} ends in"
    else:
        if seasontype == "trophies":
            next_reset = SEASON_RESET_EPOCH
            printstr = "Trophy season resets in"
        elif seasontype == "power play":
            next_reset = POWER_PLAY_EPOCH
            printstr = "Power Play season resets in"
        else:
            print("Invalid input")
            return None
        while next_reset < datetime.now():
            next_reset += datetime(weeks=2)
        remaining = next_reset - datetime.now()
    weeks = int(remaining / timedelta(weeks=1))
    days = int(remaining / timedelta(days=1)) % 7
    hours = int(remaining / timedelta(hours=1)) % 24
    mins = int(remaining / timedelta(minutes=1)) % 60
    if weeks > 0:
        print(printstr, f"{weeks}w {days}d {hours}h {mins}m.")
    else:
        print(printstr, f"{days}d {hours}h {mins}m.")


def int_assignment(prompt, variable):
    while True:
        response = input(prompt)
        if response == "":
            return
        try:
            response = int(response)
        except ValueError:
            print("Please enter a numeric value.")
            continue
        except:
            print("Unknown error.")
            continue
        else:
            variable = response
            return


def bool_input(prompt):
    response = input(prompt)
    return response.lower() == 'y'


def pp_input(prompt):
    while True:
        response = input(prompt)
        if response.lower() == 'x':
            return sum(POINTS)
        elif response == "":
            return -1
        try:
            response = int(response)
        except ValueError:
            print("Invalid input.")
            continue
        except:
            print("Unknown error.")
            continue
        else:
            return response


# ========== Resets ============================================================
def brawl_pass_reset(tier, brawlpass):
    with open("BrawlStars/seasondata.json") as f:
        seasondata = load(f)['seasons'][-1]
    print_time_remaining("brawl pass", seasondata['number'], seasondata['name'])
    rewards = seasondata['rewards']

    def translate(rewardstring):
        if rewardstring == "":
            return 0
        elif rewardstring[0] == 'b':
            return int(BRAWL_BOX * int(rewardstring[1:]))
        elif rewardstring[0] == 'c':
            return int(rewardstring[1:])
        elif rewardstring[0] == 'p':
            return 2 * int(rewardstring[1:])
    
    for r in range(len(rewards)):
        rewards[r] = [translate(s) for s in rewards[r].split('/')]
    rewards = list(zip(*rewards))  # Unzips
    remaining_prog = int(sum(rewards[0][tier:]))
    if brawlpass:
        remaining_prog += int(sum(rewards[1][tier:]))
    print(
        f"You are expected to earn another {remaining_prog} in progression " +
        f"this season."
    )
    

def trophy_reset():
    pass


def power_play_reset():
    pass


# ========== Updating ==========================================================
def player_update(playerdata, override=False):
    """
    Modifies the provided dict with custom player data.
    """
    # Request brawler data from server
    BRAWLERS = apirequest("brawlers")['items']

    def max_brawler(name):
        """ Returns the parameters for a maxed brawler. """
        for b in BRAWLERS:
            if b["name"] == name:
                return b
        return None
    
    # Initialize values, if not exist
    if 'coins' not in playerdata:
        playerdata['coins'] = 0
    if 'brawlpass' not in playerdata:
        playerdata['brawlpass'] = None
    if 'tier' not in playerdata:
        playerdata['tier'] = 1
    if 'currentseason' not in playerdata:
        playerdata['currentseason'] = CURRENT_SEASON
    # Reset calculated values
    playerdata['coins_needed'] = 0
    playerdata['points_needed'] = 0
    playerdata['sp_needed'] = [0, 0]  # SPs on brawlers
    playerdata['gadgets_needed'] = [0, 0]
    # Update values
    print(
        "Please enter the following values. " +
        "Press enter to keep existing values."
    )
    int_assignment(f"Coins: {playerdata['coins']} ", playerdata['coins'])
    if (override or playerdata['currentseason'] != CURRENT_SEASON
        or playerdata['brawlpass'] is None):
        playerdata['brawlpass'] = bool_input(f"Do you have the brawl pass? ")
    int_assignment(f"Season tier: {playerdata['tier']} ", playerdata['tier'])
    playerdata['currentseason'] = CURRENT_SEASON
    # Update brawler points
    print(
        "Please sort your brawlers by rarity and enter power points when " +
        "prompted. \nYou may also type 'x' or a large value (>1500) to set " +
        "to max value."
    )
    for b in playerdata['brawlers']:
        # Count SPs, gadgets
        total_sp = len(max_brawler(b['name'])['starPowers'])
        total_gadgets = len(max_brawler(b['name'])['gadgets'])
        if b['power'] >= 9 and total_sp > len(b['starPowers']):
            playerdata['sp_needed'][0] += total_sp - len(b['starPowers'])
            playerdata['sp_needed'][1] += 1
        if b['power'] >= 7 and total_gadgets > len(b['gadgets']):
            playerdata['gadgets_needed'][0] += total_gadgets - len(b['gadgets'])
            playerdata['gadgets_needed'][1] += 1
        # Add points
        # print(b['points'], sum(POINTS[b['power']:]))
        if 'points' not in b:
            b['points'] = 0
        if b['power'] >= 9 or b['points'] == sum(POINTS[b['power']:]):
            print(f"{b['name']} is maxed")
        else:
            pp = pp_input(
                f"{b['name']} ({b['points']}/{POINTS[b['power']]}): "
            )
            if pp >= 0:
                b['points'] = min(pp, sum(POINTS[b['power']:]))
        playerdata['points_needed'] += sum(POINTS[b['power']:])-b['points']
        playerdata['coins_needed'] += sum(COINS[b['power']:])
            
    print(
        f"Brawler data updated. You have {len(playerdata['brawlers'])}/" +
        f"{len(BRAWLERS)} brawlers."
    )
    print(
        f"You are waiting on {playerdata['sp_needed'][0]} star powers on " +
        f"{playerdata['sp_needed'][1]} brawlers."
    )
    print(
        f"You are waiting on {playerdata['gadgets_needed'][0]} gadgets on " +
        f"{playerdata['gadgets_needed'][1]} brawlers."
    )
    print(
        f"You still need {playerdata['coins_needed']} coins and " +
        f"{playerdata['points_needed']} points to max out your brawlers," +
        f" for a total of",
        playerdata['coins_needed'] + 2 * playerdata['points_needed'],
        f"progression."
    )
    brawl_pass_reset(playerdata['tier'], playerdata['brawlpass'])


def dict_merge(dict1, dict2):
    """
    Updates dict1 with dict2's values. Does deep merging on brawlers.
    Assumes dict1 >= dict2, i.e. dict2's keys are all in dict1.
    """
    retdict = {}
    for k in dict1.keys():
        if k in dict2.keys():
            retdict[k] = dict2[k]
        else:
            retdict[k] = dict1[k]
    for b1 in retdict['brawlers']:
        for b2 in dict1['brawlers']:
            if b1['name'] == b2['name'] and 'points' in b2:
                b1['points'] = b2['points']
                break
    return retdict


def update(playertag):
    """
    Updates player data from server. Optionally calls player_update.
    """
    datapath = f'BrawlStars/PlayerData/{playertag}.json'
    playerdata = {}
    # Create file if not exists, read information if exists
    if not Path(datapath).is_file():
        Path(datapath).touch()
    else:
        with open(datapath) as f:
            playerdata = load(f)
    # Update playerdata dictionary with information from server
    playerdata = dict_merge(playerdata, get_playerdata(playertag))
    print(f"Now starting calculations for {playerdata['name']}...")
    # Update
    player_update(playerdata)
    # Write back to file
    with open(datapath, 'w') as f:
        dump(playerdata, f)
    

update("UULVQY2L")
