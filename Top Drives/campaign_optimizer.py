from collections import Counter
from json import load


def test_reduction():
    with open("campaign.json") as f:
        campaign = [
            d for d in load(f)
            if d["name"][:2] not in ["SN", "YB"]
        ]
    with open("campaign_reqs.json") as f:
        reqs = load(f)

    campaign = {
        f"{loc['name']} {idx+1}": [race["name"] for race in match["races"]]
        for loc in campaign
        for idx, match in enumerate(loc["matches"])
    }

    race_counter = Counter([
        race
        for loc, match in campaign.items()
        for race in match
    ])

    # Manual adjustment
    reqs["UK Midlands"][6] = 0

    # Remove races which are blocked by reqs
    for loc, race_reqs in reqs.items():
        for idx, nblockers in enumerate(race_reqs):
            match_name = f"{loc} {idx+1}"
            match = campaign[match_name]
            pos = len(match) - 1
            while nblockers > 0:
                race_name = match[pos]
                if race_counter[race_name] > 1:
                    if pos + 1 == len(match):
                        match.pop(pos)
                    else:
                        match[pos] = ""
                    race_counter[race_name] -= 1
                    nblockers -= 1
                pos -= 1
    
    # Remove entire matches where possible
    for loc, match in campaign.items():
        counts = [race_counter[race] > 1 for race in match]
        if all(counts):
            race_counter.subtract(match)
            campaign[loc] = []
    
    # Remove duplicated races

    for i in range(4, -1, -1):
        for loc, match in campaign.items():
            if i < len(match) and race_counter[match[i]] > 1:
                race_counter[match[i]] -= 1
                if i + 1 == len(match):
                    match.pop(i)
                else:
                    match[i] = ""
    
    campaign = {k: v for k, v in campaign.items() if v and any(v)}

    max_len_name = max([len(loc) for loc in campaign])

    output = []
    for loc, match in campaign.items():
        if loc == "UK Midlands 7":
            output.append(f"{loc:<{max_len_name}}: 1")
            output.append(f"{loc:<{max_len_name}}:  2")
            continue
        race_nums = [
            str(idx+1) if match[idx] else ' '
            for idx in range(len(match))
        ]
        output.append(
            f"{loc:<{max_len_name}}: "
            f"{''.join(race_nums)}"
        )
    
    for line in output:
        print(line)
    
    with open("output.txt", "w") as f:
        f.write("\n".join(output))



test_reduction()
