from collections import deque
from json import load

import streamlit as st


def value(cash, ceram):
    return cash + 32500 * ceram


def est_cash_equiv(rewards):
    cash_value=[
        st.session_state.get("epic_frag_value", 180000),
        st.session_state.get("cf_frag_value", 42250),
        32500, 1
    ]
    return sum([rewards[i] * cash_value[i] for i in range(len(cash_value))])


def outcomes(nflags, progress, access, season_name="default"):
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
    final = [[est_cash_equiv(row[0]), *row] for row in final]
    return sorted(final, key=lambda x: x[:2])[::-1]

def display_outcome(cash_equiv, rewards, final_prog, start_prog, all_chals):
    cols = st.columns([6, 4, 4, 4, 5])
    cols[0].metric(":material/local_atm: Cash Equivalent", cash_equiv)
    cols[1].metric(":material/token: Epic Tokens", rewards[0])
    cols[2].metric(":material/token: CF Tokens", rewards[1])
    cols[3].metric(":material/capture: Ceramics", rewards[2])
    cols[4].metric(":material/local_atm: Cash", rewards[3])
    cols = st.columns(9)
    for i in range(9):
        delta = final_prog[i] - start_prog[i]
        cols[i].metric(all_chals[i], final_prog[i], delta if delta else None)


with st.expander("Cash Values", icon=":material/local_atm:"):
    col1, col2 = st.columns(2)
    col1.number_input(
        "Epic fragment value", min_value=0, value=180000, step=50,
        key="epic_frag_value",
    )
    col2.number_input(
        "CF fragment value", min_value=0, value=42250, step=50,
        key="cf_frag_value"
    )

with st.form("options"):
    st.subheader("Challenge League Progress")
    st.text("")
    challenges = [
        medal + " " + tier
        for medal in ["Bronze", "Silver"]
        for tier in ["IV", "III", "II", "I"]
    ]
    cols = st.columns(2)
    for i in range(len(challenges)):
        cols[i%2].segmented_control(
            challenges[i], options=["Locked"] + list(range(0, 6)),
            default="Locked", key=challenges[i]
        )
        cols[i%2].text("")
    st.segmented_control(
        "Frontier", options=["Locked"] + list(range(0, 26)),
        default="Locked", key="Frontier"
    )
    st.text("")
    _, num_col, _ = st.columns([3, 2, 3])
    num_col.number_input(
        "Flags remaining", min_value=0, step=1, key="flags_remaining"
    )
    _, submit_col, _ = st.columns([3, 4, 3])
    if submit_col.form_submit_button(
        "Calculate!", type="primary", use_container_width=True
    ):
        all_chals = challenges + ["Frontier"]
        progress = [
            0 if st.session_state[chal] == "Locked" else st.session_state[chal]
            for chal in all_chals
        ]
        access = [
            int(st.session_state[chal] != "Locked")
            for chal in all_chals
        ]
        results = outcomes(
            nflags=st.session_state["flags_remaining"],
            progress=progress, access=access,
        )
        display_outcome(*results[0], progress, all_chals)
        for row in results:
            st.text(row)