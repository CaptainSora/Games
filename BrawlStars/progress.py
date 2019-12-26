import brawlstats
from json import load, dump
from math import ceil
from datetime import date, timedelta

""" GAME CONSTANTS """
#         0  1   2   3   4    5    6    7    8     9  10
POINTS = [0, 20, 30, 50, 80,  130, 210, 340, 550,  0, 0]
COINS = [00, 20, 35, 75, 140, 290, 480, 800, 1250, 0, 0]
TOTAL_BRAWLERS = 31  # May need updating


def is_max(brawler):
    """ Checks if this is a maxed brawler. """
    return (sum(POINTS[brawler['power']:10]) == brawler['points'])


def upgradable(brawler):
    """ Returns the coins necessary for immediate upgrade. """
    points = brawler['points']
    power = brawler['power']
    coincost = 0
    while points >= POINTS[power] and power < 9:
        coincost += COINS[power]
        points -= POINTS[power]
        power += 1
    return coincost


def retrieve(player, brawler):
    """
    Returns a tuple of information about a brawler.
    (power, len(starpowers), trophies) all ints
    """
    for b in player.brawlers:
        if b.name == brawler:
            return (int(b.power), len(b.starPowers), int(b.trophies))


def num_input(prompt, dict, key):
    """
    Only accepts numeric or blank inputs.
    Modifies dict[key] value in-place for non-blank inputs.
    """
    while True:
        i = input(prompt)
        if i == "":
            return
        elif i.isdigit():
            dict[key] = int(i)
            return


def connect():
    # Load API Token
    with open('BrawlStars/token.txt', 'r') as tokenfile:
        token = tokenfile.read()

    # Initialize connection with Brawl Stars API
    print("Connecting to Brawl Stars API...")
    client = brawlstats.OfficialAPI(token)
    print("Connected!")
    return client


def update(playertag, player=None):
    """
    Updates the saved data for the player from Brawl API and manual input.
    """
    # Initialize connection with Brawl Stars API
    if player is None:
        client = connect()
        player = client.get_player(playertag)

    # Load saved player data
    with open('BrawlStars/data.json', 'r') as datafile:
        data = load(datafile)

    # Create framework if necessary:
    if playertag not in data:
        data[playertag] = {
            "ign": input("What is your IGN? "),
            "coins": 0,
            "starpoints": 0,
            "tickets": 0,
            "points_to_go": 0,
            "coins_needed": 0,
            "coins_to_go": 0,
            "last_updated": 0,
            "brawlers": {}
        }

    # Initialize shortcuts
    p_data = data[playertag]
    b_data = p_data['brawlers']

    # Instructions
    print("Please sort your brawlers by Most Trophies.")
    print("Enter values when prompted or press Enter to leave unchanged.")

    # Update number of coins, star points, tickets
    num_input(f"Coins: {p_data['coins']} ", p_data, 'coins')
    num_input(f"Star Points: {p_data['starpoints']} ", p_data, 'starpoints')
    num_input(f"Event Tickets: {p_data['tickets']} ", p_data, 'tickets')

    # Check for new brawlers
    for brawler in player.brawlers:
        if brawler.name not in b_data:
            b_data[brawler.name] = {
                'points': 0,
                'power': brawler.power,
                'nSP': len(brawler.starPowers),
                'trophies': brawler.trophies
            }

    # Create sorted list of updatable brawlers
    b_by_tphy = [(b.name, b.trophies, b.power) for b in player.brawlers]
    b_by_tphy.sort(key=lambda x: int(x[1]), reverse=True)

    # Update brawler data
    for b in b_by_tphy:
        brawler = b_data[b[0]]
        name = b[0]
        power = b[2]

        # Power points (auto)
        if power >= 9:
            brawler['points'] = 0

        # Power points (manual)
        if is_max(brawler):
            print(f"{name} is maxed")
        else:
            num_input(
                f"{name}: {brawler['points']}/{POINTS[power]} -> ",
                brawler, 'points'
            )

        # Other data (from server)
        info = retrieve(player, name)
        brawler['power'] = info[0]
        brawler['nSP'] = info[1]
        brawler['trophies'] = info[2]

    # Calculate coins, points needed
    p_data['coins_to_go'] = \
        sum([sum(COINS[b_data[b]['power']:10]) for b in b_data])
    p_data['coins_needed'] = \
        sum([upgradable(b_data[b]) for b in b_data])
    p_data['points_to_go'] = \
        sum([sum(POINTS[b_data[b]['power']:10]) - b_data[b]['points']
            for b in b_data])

    # Update date info
    p_data['last_updated'] = str(date.today())

    # Save to file
    with open('BrawlStars/data.json', 'w') as datafile:
        dump(data, datafile)
    print(f"Update complete. Saved {p_data['ign']} to file.")


def prediction(playertag, out_type="boxes", manual=None):
    """
    Returns predictions on when the account will be maxed.
    Output type "boxes": Returns the estimated number of brawl boxes necessary
    Output type "boxesplus": Returns more data on boxes
    Output type "date": Returns the estimated date
    Output type "dateplus": Returns more data on date

    Manual calculation: input coins and points
    """
    # CONSTANTS
    PPB = 15.1  # Points per box - Credit: KairosTime
    CPB = 23.5  # Coins per box  - Credit: KairosTime
    token_reset = 144
    star_token_events = 6
    tix_per_box = 0.362  # Estimated from KT's (not) Leon video
    doublers_per_box = 2 * 0.03  # Calculated from in-game odds
    tix_per_day = 2/7
    boxes_per_tix = 0.27  # 5:00 Robo Rumble Time
    brawlboxPD = sum([
        (24 * 60 / token_reset * 0.2),  # 20 tokens per 2h 24m
        (star_token_events * 0.1),      # 10 tokens per event
        (tix_per_day * boxes_per_tix)   # 2 tickets per ticket event
    ])
    brawlboxPD *= (1 + doublers_per_box) * (1 + tix_per_box * boxes_per_tix)
    bigboxPD = (star_token_events * 0.1 * 3)
    BPD = brawlboxPD + bigboxPD
    CPB_maxed = 70  # From KT's (not) Leon video
    CPD_maxed = brawlboxPD * CPB_maxed + bigboxPD * (2 * PPB + CPB)

    # Open file
    with open('BrawlStars/data.json', 'r') as datafile:
        data = load(datafile)
    points_to_go = data[playertag]['points_to_go']
    coins_to_go = data[playertag]['coins_to_go'] - data[playertag]['coins']

    # Manual entry
    if manual is not None:
        coins_to_go = manual[0] - data[playertag]['coins']
        points_to_go = manual[1]

    # Calculated values
    boxes_for_points = ceil(points_to_go / PPB)
    extra_coins_needed = coins_to_go - boxes_for_points * CPB
    boxes_for_coins = \
        max(0, ceil(extra_coins_needed / CPB_maxed))
    total_boxes = boxes_for_points + boxes_for_coins
    boxes_from_tix = int(data[playertag]['tickets'] * boxes_per_tix)
    days_for_points = timedelta(days=boxes_for_points / BPD)
    days_for_coins = \
        timedelta(days=max(0, extra_coins_needed / CPD_maxed))
    tix_days_saved = timedelta(days=(boxes_from_tix / BPD))
    total_days = days_for_points + days_for_coins - tix_days_saved
    today = date.today()

    if out_type == "boxes":
        return total_boxes
    elif out_type == "boxesplus":
        return [boxes_for_points, boxes_for_coins, total_boxes]
    elif out_type == "date":
        return str(today + total_days)
    elif out_type == "dateplus":
        return [str(today + days_for_points), str(today + total_days)]


def diff(playertag, delta_coins, delta_points):
    """
    Returns the estimated number of boxes saved.
    delta_coins: the change in coins (negative for spending)
    delta_points: the change in points (positive for gaining)
    """
    # From calculations, buying 23.75 power points saves 1 box of progression.
    with open('BrawlStars/data.json', 'r') as datafile:
        data = load(datafile)

    coins_new = data[playertag]['coins_to_go'] - delta_coins
    points_new = data[playertag]['points_to_go'] - delta_points
    pred_boxes_cur = prediction(playertag)
    pred_boxes_new = prediction(playertag, manual=[coins_new, points_new])

    print(
        f"That will save you {pred_boxes_cur - pred_boxes_new} boxes."
    )


# Still need season reset time
def season_reset(b_data, output='print'):
    """
    Optionally prints and returns some relevant information on the season
    reset.
    """
    SP_FLOOR = 550
    SP_CEIL = 1400
    trophy_loss = 0
    star_points = 0
    brawlers_loss = 0
    for b in b_data:
        trophies = b_data[b]['trophies']
        sp_adjust = [0, 50, 80, 100, 120]
        if trophies < SP_FLOOR:
            continue
        elif trophies >= SP_CEIL:
            trophy_loss += trophies - 950
            star_points += 480
            continue
        trophy_tier = ceil((trophies - SP_FLOOR + 1) / 50)
        trophy_loss += trophies % 50 + trophy_tier * 25
        star_points += trophy_tier * 20 + sp_adjust[min(trophy_tier, 4)]
        brawlers_loss += 1
    if output == 'print':
        print(
            f"At the end of the season, you will lose {trophy_loss} trophies" +
            f" on {brawlers_loss} brawler(s) in exchange for {star_points} " +
            f"star points."
        )
    return (trophy_loss, star_points)


def push_trophies():
    pass


def push_star_points():
    pass


def brawlerdata(player, b_data):
    """
    Prints some relevant information about the player's brawlers.
    Used in playerdata.
    """
    # Calculate values
    brawlers_owned = len(player.brawlers)
    need_pts = len([b for b in b_data if not is_max(b_data[b])])
    no_pts_brawlers = [
        b for b in b_data if b_data[b]['power'] < 9 and is_max(b_data[b])]
    p9_brawlers = [b for b in b_data if b_data[b]['power'] >= 9]
    p10_brawlers = [b for b in b_data if b_data[b]['power'] == 10]
    p10sp2_brawlers = [b for b in b_data if b_data[b]['nSP'] == 2]
    star_powers = sum([b_data[b]['nSP'] for b in b_data])
    upgr_brawlers = [
        b for b in b_data if b_data[b]['points'] > 0
        and b_data[b]['points'] >= POINTS[b_data[b]['power']]
    ]
    power_dist = [
        len([b for b in b_data if b_data[b]['power'] == x])
        for x in range(1, 11)
    ]

    # Brawler data
    print(f"You currently have {brawlers_owned}/{TOTAL_BRAWLERS} brawlers.")
    print(f"You still need power points for {need_pts} brawlers.")
    print(
        f"You currently have {len(p10_brawlers)} brawlers at Power 10: " +
        f"{', '.join(p10_brawlers)}"
    )
    print(
        f"You are still waiting for {2 * len(p9_brawlers) - star_powers} " +
        f"star powers on {len(p9_brawlers) - len(p10sp2_brawlers)} brawler(s)."
    )
    print(
        f"The following {len(upgr_brawlers)} brawlers are ready to be " +
        f"upgraded: {', '.join(upgr_brawlers)}"
    )
    print(
        f"The following {len(no_pts_brawlers)} brawlers are ready to be " +
        f"upgraded to power 9: {', '.join(no_pts_brawlers)}"
    )
    print(
        f"Your brawlers' power levels are distributed as follows: {power_dist}"
    )


# Skins, Star Points
# How many tilted trophies, most tilted brawler (above and below 550 at max)
def playerdata(playertag):
    """ Prints some relevant information about the player. """
    with open("BrawlStars/data.json", 'r') as datafile:
        data = load(datafile)
    try:
        p_data = data[playertag]
        b_data = p_data['brawlers']
    except KeyError:
        update(playertag)
        playerdata(playertag)
        return

    # Initialize connection with Brawl Stars API
    client = connect()
    player = client.get_player(playertag)
    print(f"Now starting calculations for {p_data['ign']}.")

    # Calculate numbers
    cur_trophies_saved = sum([b_data[b]['trophies'] for b in b_data])
    cur_trophies = player.trophies

    # Check for update and update variables
    if cur_trophies_saved != cur_trophies:
        i = input("Saved data expired! Update? [y/n] ")
    else:
        i = input("Would you like to update? [y/n] ")
    if i.lower() == 'y':
        update(playertag, player=player)
    with open("BrawlStars/data.json", 'r') as datafile:
        data = load(datafile)
    p_data = data[playertag]
    b_data = p_data['brawlers']

    # Continue calculating numbers post-update
    max_trophies = player.highest_trophies
    max_possible_trophies = sum([b.highest_trophies for b in player.brawlers])
    points_to_go = p_data['points_to_go']
    coins_to_go = p_data['coins_to_go'] - p_data['coins']
    boxes_to_max = prediction(playertag, out_type='boxes')
    date_to_max = prediction(playertag, out_type='date')

    # Basic Information
    print(f"You currently have {cur_trophies} trophies.")
    print(f"At your peak, you had {max_trophies} trophies.")
    print(
        f"If all your brawlers were at their highest trophies, you would" +
        f" have {max_possible_trophies} trophies."
    )
    print(
        f"You need another {points_to_go} power points for your current " +
        f"brawlers."
    )
    print(
        f"You need another {coins_to_go} coins to upgrade all your brawlers" +
        f" to power 9."
    )
    print(
        f"You are estimated to max your account (not including star powers) " +
        f"on {date_to_max} after approximately {boxes_to_max} brawl boxes."
    )

    # Brawler Information
    i = input("Would you like more information about your brawlers? [y/n] ")
    if i.lower() == 'y':
        brawlerdata(player, b_data)

    # Season Reset Information
    i = input("Would you like more information about season reset? [y/n] ")
    if i.lower() == 'y':
        season_reset(b_data)


def playertags(player=None):
    with open('BrawlStars/data.json', 'r') as datafile:
        data = load(datafile)
    taglist = [(pt, data[pt]['ign']) for pt in data]
    try:
        return taglist[player][0]
    except (TypeError, IndexError):
        return taglist


print(playertags())
playerdata(playertags(0))
