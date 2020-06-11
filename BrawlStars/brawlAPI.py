from datetime import datetime, timedelta
from json import dump, load, loads
from pathlib import Path

from requests import get


""" TO DO """
# BP Track replacements
#   Seems like all PP replaced with Big box; at least true up to 100 PP
# How much money would be required to max account, using 80 gem mega boxes
#   Might have to save brawler rarities somewhere, and legendary drop rates
# Optional: unclaimed from tier


""" TO FIX """
# Season end dates + times
# Magic numbers (e.g. T61)
# DOCSTRINGS YOU LAZY PIECE OF SH!T


""" SORT ORDER """
BRAWLER_ORDER = [
    'SHELLY', 'NITA', 'COLT', 'BULL', 'JESSIE', 'BROCK',
    'DYNAMIKE', 'BO', 'TICK', '8-BIT', 'EMZ', 'EL PRIMO',
    'BARLEY', 'POCO', 'ROSA', 'RICO', 'DARRYL', 'PENNY',
    'CARL', 'JACKY', 'PIPER', 'PAM', 'FRANK', 'BIBI',
    'BEA', 'MORTIS', 'TARA', 'GENE', 'MAX', 'MR.P',
    'SPROUT', 'SPIKE', 'CROW', 'LEON', 'SANDY', 'GALE'
]
""" GAME CONSTANTS """
#        0  1   2   3   4    5    6    7    8    9  10
POINTS = [0, 20, 30, 50, 80, 130, 210, 340, 550, 0, 0]
COINS = [0, 20, 35, 75, 140, 290, 480, 800, 1250, 0, 0]
RESETDATA = [
    [550, 525, 70],
    [600, 575, 120],
    [650, 625, 160],
    [700, 650, 200],
    [750, 700, 220],
    [800, 750, 240],
    [850, 775, 260],
    [900, 825, 280],
    [950, 875, 300],
    [1000, 900, 320],
    [1050, 925, 340],
    [1100, 950, 360],
    [1150, 975, 380],
    [1200, 1000, 400],
    [1250, 1025, 420],
    [1300, 1050, 440],
    [1350, 1075, 460],
    [1400, 1100, 480],
    [10000, 0, 0]
]
PPDATA = [
    [0, 0],
    [99, 25],
    [149, 50],
    [199, 100],
    [249, 150],
    [299, 200],
    [349, 250],
    [399, 300],
    [449, 350],
    [499, 400],
    [549, 450],
    [599, 500],
    [649, 550],
    [699, 600],
    [749, 700],
    [799, 800],
    [849, 1000],
    [899, 1500],
    [949, 2000],
    [999, 2500],
    [1049, 3000],
    [1099, 4000],
    [1149, 5000],
    [1199, 6000],
    [1249, 8000],
    [10000, 10000]
]
""" GAME VARIABLES """
CURRENT_SEASON = 1
SEASON_OFFSET = 5
SEASON_1_END = datetime(2020, 7, 6, SEASON_OFFSET)
SEASON_RESET_EPOCH = datetime(2020, 5, 4, 4)
POWER_PLAY_EPOCH = datetime(2020, 5, 11, 22)
""" PROGRESSION VALUES """
BRAWL_BOX = 53.7
BIG_BOX = 3 * BRAWL_BOX


# ========== Data from server =================================================
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
    HTTPS_RESPONSES = {
        400: "Client provided incorrect parameters for the request.",
        403: "Access denied.",
        404: "Resource not found.",
        429: "Request was throttled.",
        500: "Unknown error.",
        503: "Service is unavailable due to maintenance."
    }
    print(f"Error code: {response.status_code}")
    if response.status_code in HTTPS_RESPONSES:
        print(HTTPS_RESPONSES[response.status_code])
    return None


def get_playerdata(playertag):
    return apirequest(f"players/%23{playertag}")


# ========== Print formatting =================================================
def print_time_remaining(seasontype):
    """
    Prints the time remaining until the season ends.
    Seasontype is one of "brawlpass", "trophies", "powerplay"
    """
    if seasontype == "brawlpass":
        remaining = SEASON_1_END - datetime.now()
        with open("BrawlStars/seasondata.json") as f:
            seasondata = load(f)['seasons'][-1]
        printstr = (
            f"\n=== Season {seasondata['number']}: {seasondata['name']} "
            f"ends in"
        )
    else:
        if seasontype == "trophies":
            next_reset = SEASON_RESET_EPOCH
            printstr = "\n=== Trophy season resets in"
        elif seasontype == "powerplay":
            next_reset = POWER_PLAY_EPOCH
            printstr = "\n=== Power Play season resets in"
        else:
            print("Invalid input")
            return None
        while next_reset < datetime.now():
            next_reset += timedelta(weeks=2)
        remaining = next_reset - datetime.now()
    weeks = int(remaining / timedelta(weeks=1))
    days = int(remaining / timedelta(days=1)) % 7
    hours = int(remaining / timedelta(hours=1)) % 24
    mins = int(remaining / timedelta(minutes=1)) % 60
    if weeks > 0:
        print(printstr, f"{weeks}w {days}d {hours}h {mins}m. ===")
    else:
        print(printstr, f"{days}d {hours}h {mins}m. ===")


def int_input(prompt, prev_value=0):
    while True:
        response = input(prompt)
        if response == "":
            return prev_value
        try:
            response = int(response)
        except ValueError:
            print("Please enter a numeric value.")
            continue
        else:
            return response


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
        else:
            return response


# ========== Resets ===========================================================
def season_rewards(convert=False, brawlerlist=[]):
    """
    Generates brawl pass rewards from seasondata.json
    First list is F2P track, second is Brawl Pass track, third is token cost
    convert does alternate reward conversion
    brawlerlist is necessary with convert=True
    """
    # Load data
    with open("BrawlStars/seasondata.json") as f:
        seasondata = load(f)['seasons'][-1]
    rewards = seasondata['rewards']
    cost = seasondata['cost']

    # Convert stored datatype to progression
    def translate(rewardstring):
        if rewardstring == "":
            return 0
        elif rewardstring[0] == 'b':
            return BRAWL_BOX * int(rewardstring[1:])
        elif rewardstring[0] == 'c':
            return int(rewardstring[1:])
        elif rewardstring[0] == 'p':
            if convert:
                return BIG_BOX
            else:
                return 2 * int(rewardstring[1:])
        elif rewardstring[0] == 'n':
            if convert and rewardstring[1:] in brawlerlist:
                return BIG_BOX
            else:
                return 0
        else:
            return 0

    for r in range(len(rewards)):
        rewards[r] = [translate(s) for s in rewards[r].split('/')]
    return list(zip(*rewards)) + [cost]  # Unzips


def brawl_pass_reset(tier, brawlpass, rewards):
    print_time_remaining("brawlpass")
    # Calculate progression left in season
    tokens = tokens_remaining(brawlpass)
    if tokens > int(sum(rewards[2][tier:])):
        big_boxes = int((tokens - sum(rewards[2][tier:])) / 500)
        remaining_prog = sum(rewards[0][tier:]) + \
            (sum(rewards[1][tier:]) if brawlpass else 0) + BIG_BOX * big_boxes
    else:
        remaining_prog = 0
        big_boxes = 0
        cur_tier = tier  # Guaranteed to stay <= 60
        while True:
            if tokens < rewards[2][cur_tier]:
                break
            remaining_prog += rewards[0][cur_tier] + \
                (rewards[1][cur_tier] if brawlpass else 0)
            tokens -= rewards[2][cur_tier]
            cur_tier += 1
    print(
        f"You are expected to open {int(big_boxes)} big boxes at the end of "
        f"the season."
    )
    return int(remaining_prog)


def trophy_reset(brawlers, cur_trophies):
    trophy_loss = 0
    star_points = 0
    brawlers_loss = 0
    for b in brawlers:
        # Earns no star points
        if b['trophies'] < RESETDATA[0][0]:
            continue
        for r in range(len(RESETDATA)):
            if b['trophies'] < RESETDATA[r][0]:
                trophy_loss += b['trophies'] - RESETDATA[r-1][1]
                star_points += RESETDATA[r-1][2]
                brawlers_loss += 1
                break
    print_time_remaining("trophies")
    print(
        f"At the end of the season, you will lose {trophy_loss} trophies"
        f" on {brawlers_loss} brawler(s) in exchange for {star_points} "
        f"star points."
    )
    print(f"This will leave you at {cur_trophies - trophy_loss} trophies.")


def power_play_reset(ppp):
    star_points = 0
    for r in PPDATA:
        if ppp <= r[0]:
            star_points = r[1]
            break
    print_time_remaining("powerplay")
    print(
        f"You currently have {ppp} power play trophies which will earn you "
        f"{star_points} star points at the end of the season."
    )


# ========== Progression ======================================================
def tokens_remaining(brawlpass):
    remaining = SEASON_1_END - datetime.now()
    token_bank_remaining = int(10 * (remaining / timedelta(days=1))) * 20
    small_q_remaining = int(remaining / timedelta(days=1)) * 2 * 100
    weekday = (datetime.now() - timedelta(hours=5)).weekday()
    EST_QUEST_TOKENS = 1000  # Averaging 2000 tokens per week, 1000 each reset
    medlg_q_remaining = (EST_QUEST_TOKENS + (250 if brawlpass else 0)) * \
        (
            2 * int(remaining / timedelta(weeks=1))
            + (1 if weekday < 3 else 0)
            + (1 if weekday == 0 else 0))
    weekly_q_remaining = 500 * (
        int(remaining / timedelta(weeks=1)) + (1 if weekday < 5 else 0))
    NEW_EVENTS = 5
    new_event_tokens = NEW_EVENTS * int(remaining / timedelta(days=1))
    addl_tokens = 0
    if bool_input("Would you like to add additional token data? (y) "):
        print("Press enter for a value of 0.")
        tier_prog = int_input("What is your progress on your current tier? ")
        bank_tokens = int_input("How many tokens do you have in bank? ")
        q_tokens = int_input("How many tokens can you still earn in quests? ")
        doublers = int_input("How many token doublers do you have? ")
        addl_tokens += tier_prog + bank_tokens + q_tokens + \
            min(doublers, token_bank_remaining + bank_tokens)
    return token_bank_remaining + small_q_remaining + medlg_q_remaining + \
        weekly_q_remaining + addl_tokens + new_event_tokens


def total_season_prog(brawlpass):
    # Track progression
    rewards = season_rewards()
    prog = int(sum(rewards[0]) + (sum(rewards[1]) if brawlpass else 0))
    # T61 (bonus) progression
    season_cost = sum(rewards[2])
    # Daily: 200 bank, 200 quests, 50 new events
    # Weekly: Assume 8 weeks per season, 2000 med/lg quests, 500 weekly,
    #   500 brawl pass exclusive
    season_tokens = 60 * 450 + 8 * (2500 + (500 if brawlpass else 0))
    bonus_prog = BIG_BOX * int((season_tokens - season_cost) / 500)
    return prog + bonus_prog


def max_brawlers(prog_to_max, prog_in_season, sp_left=0, gadgets_left=0):
    season_prog = [total_season_prog(False), total_season_prog(True)]
    endstr = ["at power 9", "fully maxed"]
    prog = prog_to_max
    for i in range(len(endstr)):
        if i == 1:
            prog = prog_to_max + 2000 * sp_left + 1000 * gadgets_left
        if prog > prog_in_season:
            # Maxed in future season
            prog_left = prog - prog_in_season
            season_req = [int(prog_left / p) + 1 for p in season_prog]
            if season_req[0] == season_req[1]:
                print(
                    f"You should have all current brawlers {endstr[i]} by the "
                    f"end of season {CURRENT_SEASON + season_req[0]}."
                )
            else:
                print(
                    f"You should have all current brawlers {endstr[i]} by the "
                    f"end of season {CURRENT_SEASON + season_req[1]} with the "
                    f"brawl pass, or the end of season "
                    f"{CURRENT_SEASON + season_req[0]} without the brawl pass."
                )
        else:
            # Maxed in current season
            print(
                f"You should have all current brawlers {endstr[i]} by the end "
                f"of this season."
            )


def to_dollars(progression):
    return 13.99 / 170 * 80 * progression / (10 * BRAWL_BOX)


# ========== Updating =========================================================
def player_update(pdata, verbose=True, override=False):
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
    if 'coins' not in pdata:
        pdata['coins'] = 0
    if 'brawlpass' not in pdata:
        pdata['brawlpass'] = None
    if 'tier' not in pdata:
        pdata['tier'] = 1
    if 'currentseason' not in pdata:
        pdata['currentseason'] = CURRENT_SEASON
    # Reset calculated values
    old_prog = 0
    if 'coins_needed' in pdata and 'points_needed' in pdata:
        old_prog = pdata['coins_needed'] + 2 * pdata['points_needed']
    pdata['coins_needed'] = 0
    pdata['points_needed'] = 0
    pdata['sp_needed'] = [0, 0]  # SPs on brawlers
    pdata['gadgets_needed'] = [0, 0]
    # Update values
    print(
        "Please input the following values when prompted. "
        "Press 'enter' to keep existing values."
    )
    pdata['coins'] = int_input(f"Coins: {pdata['coins']} ", pdata['coins'])
    if (override or pdata['currentseason'] != CURRENT_SEASON
        or pdata['brawlpass'] is None):
        pdata['brawlpass'] = bool_input(f"Do you have the brawl pass? ")
    pdata['tier'] = int_input(f"Season tier: {pdata['tier']} ", pdata['tier'])
    pdata['currentseason'] = CURRENT_SEASON
    # Update brawler points
    print(
        "Please sort your brawlers by rarity and enter power points when "
        "prompted. \nYou may also type 'x' or a large value (>1500) to set "
        "to max value."
    )
    for name in BRAWLER_ORDER:
        for b in pdata['brawlers']:
            # Sort in rarity order
            if b['name'] != name:
                continue
            # Count SPs, gadgets
            total_sp = len(max_brawler(b['name'])['starPowers'])
            total_gadgets = len(max_brawler(b['name'])['gadgets'])
            if b['power'] >= 9 and total_sp > len(b['starPowers']):
                pdata['sp_needed'][0] += total_sp - len(b['starPowers'])
                pdata['sp_needed'][1] += 1
            if b['power'] >= 7 and total_gadgets > len(b['gadgets']):
                pdata['gadgets_needed'][0] += total_gadgets - len(b['gadgets'])
                pdata['gadgets_needed'][1] += 1
            # Add points
            # print(b['points'], sum(POINTS[b['power']:]))
            if 'points' not in b:
                b['points'] = 0
            if b['power'] >= 9 or b['points'] >= sum(POINTS[b['power']:]):
                b['points'] = sum(POINTS[b['power']:])
                if verbose:
                    print(f"{b['name']} is maxed")
            else:
                pp = pp_input(
                    f"{b['name']} ({b['points']}/{POINTS[b['power']]}): "
                )
                if pp >= 0:
                    b['points'] = pp
            b['points'] = min(b['points'], sum(POINTS[b['power']:]))
            pdata['points_needed'] += sum(POINTS[b['power']:])-b['points']
            pdata['coins_needed'] += sum(COINS[b['power']:])
    # ==================== Print values ====================================
    print("Brawler data updated.")
    # Collection
    print("\n=== Collection ===")
    print(f"You have {len(pdata['brawlers'])}/{len(BRAWLERS)} brawlers.")
    print(
        f"You are waiting on {pdata['sp_needed'][0]} star powers on "
        f"{pdata['sp_needed'][1]} brawlers."
    )
    print(f"You are waiting on {pdata['gadgets_needed'][0]} gadgets.")
    # Season
    rewards = season_rewards(
        convert=(pdata['points_needed'] == 0),
        brawlerlist=[b['name'] for b in pdata['brawlers']]
    )
    prog_in_season = brawl_pass_reset(
        pdata['tier'], pdata['brawlpass'], rewards
    )
    # Trophy reset
    trophy_reset(pdata['brawlers'], pdata['trophies'])
    # Power play
    power_play_reset(pdata['powerPlayPoints'])
    # Completion
    print("\n=== Completion ===")
    prog_remaining = pdata['coins_needed'] + 2 * pdata['points_needed']
        # Assumes 2 SP and 1 G per brawler
        # Should new brawlers be included?
    addl_coins = (
        2000 * pdata['sp_needed'][0]
        + 1000 * pdata['gadgets_needed'][0]
        # + 5000 * (len(BRAWLERS) - len(pdata['brawlers']))
    )
    if prog_remaining > 0:
        print(
            f"You still need {pdata['coins_needed']} coins and "
            f"{pdata['points_needed']} points to upgrade all your brawlers to "
            f"power 9, for a total of {prog_remaining} progression."
        )
    else:
        print("All your brawlers are at or above power 9.")
    if prog_remaining + addl_coins > 0:
        print(
            f"You need an additional {addl_coins} coins to buy all remaining "
            f"star powers and gadgets for your brawlers, for a total of "
            f"{prog_remaining + addl_coins} progression."
        )
        max_brawlers(prog_remaining, prog_in_season, pdata['sp_needed'][0], 
                    pdata['gadgets_needed'][0])
        print(
            f"You are expected to earn another {prog_in_season} progression "
            f"this season."
        )
    else:
        print("You have all available star powers and gadgets.")
    # For fun
    print("\n=== For fun ===")
    print(
        f"You have earned ${to_dollars(old_prog - prog_remaining):.2f} in "
        f"progression since you last updated your data."
    )
    print(
        f"Using 80 gem mega boxes and buying the most popular gem offer, it "
        f"would cost:"
    )
    print(
        f"  ${to_dollars(prog_remaining):.2f} to upgrade all current brawlers "
        f"to power 9"
    )
    print(
        f"  ${to_dollars(prog_remaining + addl_coins):.2f} to fully upgrade "
        f"all current brawlers"
    )
    print("")


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


def update(playertag, verbose=True, override=False):
    """
    Updates player data from server. Optionally calls player_update.
    """
    datapath = f'BrawlStars/PlayerData/{playertag}.json'
    playerdata = {}
    # Create file if not exists, read information if exists
    if not Path(datapath).is_file():
        Path(datapath).touch()
        playerdata = get_playerdata(playertag)
        print("Hello! Now recording first-time data.")
    else:
        with open(datapath) as f:
            playerdata = load(f)
        # Update playerdata dictionary with information from server
        playerdata = dict_merge(playerdata, get_playerdata(playertag))
        print(f"Now starting calculations for {playerdata['name']}...")
    # Update=
    player_update(playerdata, verbose, override)
    # Write back to file
    with open(datapath, 'w') as f:
        dump(playerdata, f)

update("UULVQY2L", verbose=False)
