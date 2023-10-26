from collections import deque
from json import load


def value(cash, ceram):
    return cash + 32500 * ceram


def value_printout(rewards, state):
    cash_value = [180000, 42250, 32500, 1]
    value = sum([rewards[i] * cash_value[i] for i in range(len(cash_value))])
    print(value, rewards, state)


def outcomes(nflags, progress, access, season_name):
    # Load saved data
    with open("flags.json") as f:
        flags = load(f)
        try:
            flags = flags[season_name]
        except:
            return f"Cannot find season '{season_name}'."
    
    # Validate input
    if len(progress) != len(flags):
        return f"Expected {len(flags)} rounds, got {len(progress)} rounds"
    
    # # Auto-compute accessible challenges
    # if max_challenge is None:
    #     max_challenge = max([
    #         i for i in range(len(progress))
    #         if progress[i] == max(progress)
    #     ]) + (1 if max(progress) >= 5 else 0)
    
    # Each round is saved as [cost, cash, ceramic, cf fragment, epic fragment]
    # Each state is saved as (progress, reward, max challenge, flags remaining)

    # Smart BFS search
    queue = deque([(progress, [0, 0, 0, 0], access, nflags)])
    final = {}
    while queue:
        prog, reward, cur_acc, flags_rem = queue.popleft()
        added = False
        for i in range(len(cur_acc)):
            if not (cur_acc[i] or prog[i-1] >= len(flags[i-1])):
                continue
            if prog[i] >= len(flags[i]) or flags[i][prog[i]][0] > flags_rem:
                continue
            round_reward = flags[i][prog[i]][1:]
            queue.append([
                [prog[j] + (1 if i == j else 0) for j in range(len(prog))],
                [reward[i] + round_reward[i] for i in range(len(reward))],
                cur_acc[:i+1] + [0 * (len(cur_acc) - i - 1)],
                flags_rem - flags[i][prog[i]][0]
            ])
            added = True
        if not added:
            cash, ceram, *packs = reward
            cash_value = value(cash, ceram)
            packs = tuple(packs[::-1])
            # Remove strictly worse outcomes
            if packs not in final or value(*final[packs][:2]) < cash_value:
                final[packs] = (cash, ceram, prog)
    
    # Sort outcomes by epic - cff - ceram - cash
    final = [[list(k) + [v[1]] + [v[0]]] + [v[2]] for k, v in final.items()]
    for row in sorted(final, key=lambda x: x[0])[::-1]:
        value_printout(*row)


# outcomes(273, [0, 0, 0, 0, 0, 5, 5, 0], "Circuit Breakers")
outcomes(
    74,
    [0, 0, 0, 0, 0, 0, 5, 5, 5],
    [1, 0, 0, 0, 0, 1, 0, 0, 1],
    "Living On The Edge"
)
