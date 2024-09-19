from json import load


def get_yb_sn_sr_rewards():
    with open("chsp_prizes.json") as f:
        prizes = load(f)
    with open("cars_final.json") as f:
        cars = load(f)
    # Completed rounds that cost 100 renown
    # avail = {
    #     "YB USA": 10,
    #     "YB Germany": 10,
    #     "YB UK": 10,
    #     "YB France": 10,
    #     "YB Japan": 10,
    #     "YB Italy": 10,
    #     "YB Road to YB": 0,
    #     "SN Orig 2010s": 10,
    #     "SN Orig 2000s": 9,
    #     "SN Orig 80-90s": 10,
    #     "SN JPT 10-20s": 7,
    #     "SN JPT 2000s": 10,
    #     "SN JPT 80-90s": 10,
    #     "SN Road to SN": 0
    # }
    # Completed rounds that cost 300 renown
    # Basically only those which can give URs as well
    avail = {
        "YB USA": 0,
        "YB Germany": 0,
        "YB UK": 0,
        "YB France": 0,
        "YB Japan": 0,
        "YB Italy": 0,
        "YB Road to YB": 10,
        "SN Orig 2010s": 0,
        "SN Orig 2000s": 0,
        "SN Orig 80-90s": 0,
        "SN JPT 10-20s": 0,
        "SN JPT 2000s": 0,
        "SN JPT 80-90s": 0,
        "SN Road to SN": 0
    }
    # Extract car names
    prize_names = []
    for d in prizes:
        prize_names.extend([
            car
            for round in d["matches"][:avail[d["name"]]]
            for car in round
        ])
    prize_names = set(prize_names)
    # Filter for SR prizes
    sr_prizes = []
    for car in cars:
        if car["class"] != "C":
            continue
        if car["rid"] in prize_names:
            sr_prizes.append((car["rq"], car["name"], car["year"]))
    sr_prizes.sort(key=lambda x: (-x[0], x[1]), reverse=True)
    for sr in sr_prizes:
        print(f"rq{sr[0]} {sr[1]} ({sr[2]})")
    


if __name__ == "__main__":
    get_yb_sn_sr_rewards()
