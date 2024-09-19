from collections import Counter
from json import dump, load
from random import choice


def score(solution):
    return len(solution) + sum([len(solution[key]) for key in solution])


def print_results(campaign):
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
    
    # for line in output:
    #     print(line)
    return output


def reorder_solution(campaign, solution):
    new_solution = {}
    for loc in campaign:
        if loc in solution:
            new_solution[loc] = solution[loc]
    return new_solution


def read_campaign():
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
    
    with open("campaign_reqs_removed.json", "w") as f:
        dump(campaign, f)


def reduction_attempt_1():
    with open("campaign_reqs_removed.json") as f:
        campaign = load(f)
    
    race_counter = Counter([
        race
        for loc, match in campaign.items()
        for race in match
    ])
    
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

    output = print_results(campaign)
    
    optimized_score = score(campaign)
    print(optimized_score)
    
    if optimized_score < 240:
        with open(f"output_{optimized_score}.txt", "w") as f:
            f.write("\n".join(output))


def reduction_attempt_2():
    with open("campaign_reqs_removed.json") as f:
        campaign = load(f)
    
    race_counter = Counter([
        race
        for loc, match in campaign.items()
        for race in match
    ])

    covered_tracks = set()
    solution = {}
    while len(covered_tracks) < len(race_counter):
        candidates = []
        for loc, match in campaign.items():
            existing_length = 0 if loc not in solution else len(solution[loc])
            for length in range(existing_length + 1, len(match) + 1):
                submatch = match[:length]
                new_tracks = set(submatch) - covered_tracks
                cost = length - existing_length + (0 if loc in solution else 1)
                # Ensure unique tracks get added asap
                if race_counter[submatch[-1]] == 1:
                    cost = 0
                if new_tracks:
                    candidates.append((loc, submatch, new_tracks, cost))
        
        candidates.sort(key=lambda x: (x[3], -len(new_tracks), len(x[1])))

        best_loc, best_submatch, new_tracks, _ = candidates[0]
        solution[best_loc] = best_submatch
        covered_tracks.update(new_tracks)
        print(f"{len(covered_tracks)}/{len(race_counter)}")
    
    optimized_score = score(solution)
    print(optimized_score)


def reduction_attempt_3():
    with open("campaign_reqs_removed.json") as f:
        campaign = load(f)
    
    race_counter = Counter([
        race
        for loc, match in campaign.items()
        for race in match
    ])

    covered_tracks = set()
    solution = {}
    while len(covered_tracks) < len(race_counter):
        candidates = []
        for loc, match in campaign.items():
            existing_length = 0 if loc not in solution else len(solution[loc])
            for length in range(existing_length + 1, len(match) + 1):
                submatch = match[:length]
                new_tracks = set(submatch) - covered_tracks
                cost = length - existing_length + (0 if loc in solution else 1)
                # Ensure unique tracks get added asap
                if race_counter[submatch[-1]] == 1:
                    cost = 0
                if new_tracks:
                    candidates.append((loc, submatch, new_tracks, cost))
        
        candidates.sort(key=lambda x: x[3])
        min_cost = [tup for tup in candidates if tup[3] == candidates[0][3]]

        best_loc, best_submatch, new_tracks, _ = choice(min_cost)
        solution[best_loc] = best_submatch
        covered_tracks.update(new_tracks)
    
    solution = reorder_solution(campaign, solution)
    # TODO: Remove duplicate tracks
    optimized_score = score(solution)
    output = print_results(solution)
    print(optimized_score)
    
    if optimized_score < 230:
        with open(f"output_{optimized_score}.txt", "w") as f:
            f.write("\n".join(output))
    
    return optimized_score


def create_link(score):
    with open(f"output_{score}.txt") as f:
        output = f.read()
    with open("campaign_reqs_removed.json") as f:
        campaign = load(f)
    linktext = []
    base = "https://www.topdrivesrecords.com?share="
    delim = "~K"
    limit = 10
    cur_tracks = []
    cur_locs = []
    for line in output.split("\n"):
        loc, nums = line.split(": ")
        loc = loc.strip()
        nums = [int(d) - 1 for d in nums if d.isdigit()]
        selected = [campaign[loc][i] for i in nums]
        if len(cur_tracks) + len(selected) > limit:
            link = base + delim + delim.join(cur_tracks)
            linktext.extend([link] + cur_locs + [" "])
            cur_tracks = []
            cur_locs = []
        cur_tracks.extend(selected)
        cur_locs.append(line)
    if cur_tracks:
        link = base + delim + delim.join(cur_tracks)
        linktext.extend([link] + cur_locs)
    with open("TDR_links.txt", "w") as f:
        f.write("\n".join(linktext))


# read_campaign()
# reduction_attempt_1()
# reduction_attempt_2()
# for _ in range(10000):
#     optimized_score = reduction_attempt_3()
#     if optimized_score < 230:
#         break
# create_link(230)
