import json
from datetime import datetime


def EVENTLIST(index=-1):
    """
    Returns the name of the requested event.
    """
    events = [
        "ordinalbattlev1",
        "sortilienaflower",
        "kiritoeugeostyle",
        "cathedralassaultv1",
        "rosegardenpart1"
    ]
    if 0 <= index < len(events):
        return events[index]
    return events


def eventcost(eventname):
    """
    Returns the event currency cost of all wanted items in the event exchange.
    """
    with open(f'SAOARS/{eventname}.json') as f:
        eventdata = json.load(f)
    cost = 0
    for a in eventdata["items"]:
        x = eventdata["items"][a]
        cost += max(0, (x["left"] - x["target"]) * x["cost"])
    for b in eventdata["elemental-items"]:
        y = eventdata["elemental-items"][b]
        cost += sum([max(0, y["left"][c] - y["target"][c]) for c in range(7)]) \
            * y["cost"]
    return cost


def eventAP(eventname):
    """
    Calculates how much AP/other energy is needed to get all rewards.
    """
    with open(f'SAOARS/{eventname}.json') as f:
        eventdata = json.load(f)
    cost = eventcost(eventname)
    eventtype = eventdata['info']['type']
    info = eventdata['info']
    # Logic
    if eventtype == 'pickup':
        return cost / info['reward'] * info['apcost']
    elif eventtype == 'assault':
        return 0
    elif eventtype == 'ordinal':
        WINRATE = 0.8
        avg_rwd = WINRATE * info['w_reward'] + (1 - WINRATE) * info['l_reward']
        return cost / avg_rwd
    else:
        print("Event type not coded yet")
        return


def eventinfo(eventname=""):
    """
    Prints some info about all the events.
    """
    # Loops through every event, optionally pick one
    if eventname == '':
        eventlist = EVENTLIST()
    else:
        eventlist = [eventname]
    # Print data about all events in eventlist
    print('')
    for e in eventlist:
        with open(f'SAOARS/{e}.json') as f:
            eventdata = json.load(f)
        eventtype = eventdata['info']['type']
        if eventtype == 'pickup':
            print(
                f"You will need about {eventAP(e):.0f} AP to get all the " +
                f"rewards for {e}."
            )
        elif eventtype == 'assault':
            print("No info on assault modes yet.")
        elif eventtype == 'ordinal':
            print(
                f"At 80% winrate, you will need another {eventAP(e):.0f} " +
                f"battles to get all the rewards for {e}."
            )
        else:
            print("Event type not coded yet")
    print('')


def countdown(eventname):
    """
    Prints the remaining event time.
    """
    with open(f'SAOARS/{eventname}.json') as f:
        eventdata = json.load(f)
    end = list(map(int, eventdata['enddateUTC'].split('-')))
    countdown = datetime(end[0], end[1], end[2], end[3], end[4]) - \
        datetime.utcnow()
    return [countdown.days, int(countdown.seconds/3600)]


def rewards(eventname):
    """
    Prints the rewards still requested for the event.
    """
    # Open file
    with open(f'SAOARS/{eventname}.json') as f:
        eventdata = json.load(f)
    # Local constants and counters
    ELEMENTS = ['Non', 'Fire', 'Water', 'Earth', 'Wind', 'Light', 'Dark']
    COLORS = ['White', 'Red', 'Blue', 'Orange', 'Green', 'Yellow', 'Purple']
    counter = 1
    # Countdown
    timeleft = countdown(eventname)
    # Print
    print(f"Items for {eventname}. Total cost: {eventcost(eventname)}")
    print(f"{timeleft[0]}d {timeleft[1]}h remaining.")
    for a in eventdata['items']:
        x = eventdata['items'][a]
        if x['left'] > x['target']:
            if x['quantity'] > 1:
                quantity = f" ({x['quantity']}pc)"
            else:
                quantity = ""
            print(
                f"{counter}. " +
                f"{a}{quantity} x{x['left'] - x['target']} at " +
                f"{x['cost']} each."
            )
            counter += 1
    for b in eventdata['elemental-items']:
        y = eventdata['elemental-items'][b]
        for c in range(7):
            if y['left'][c] > y['target'][c]:
                if "Manual" in b:
                    name = f"{b} ({ELEMENTS[c]}-elem.)"
                elif "EXP" in b:
                    name = f"{b} ({ELEMENTS[c]}-elemental)"
                elif "Flower" in b or "Bud" in b or "Seed" in b:
                    name = f"{COLORS[c]} {b}"
                else:
                    name = f"!{b}!"
                if y['quantity'] > 1:
                    name += f" ({y['quantity']}pc)"
                print(
                    f"{counter}. {name} " +
                    f"x{y['left'][c] - y['target'][c]} at {y['cost']} " +
                    f"each."
                )
                counter += 1
    print('')


rewards(EVENTLIST(1))
