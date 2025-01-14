import numpy as np
import pandas as pd
import streamlit as st


cars = [None for _ in range(5)]
emojis = ["⭐", "🔴", "🟩", "🔷", "🩷"]

st.subheader("Your hand")
car_cols = st.columns(5)
for t, car_col in enumerate(car_cols):
    cars[t] = car_col.text_area(
        "Car Placement", value=None, height=68, key=f"car_input_{t}",
        placeholder=f"Car {t+1}", label_visibility="collapsed"
    )
    car_col.html(f"<h5 style='text-align: center;'>{emojis[t]}</h5>")

def swap_car(trackset: int, carnum: int) -> None:
    car = st.session_state[f"placement_{trackset}_{carnum}"]
    if car is None:
        return
    for k in range(5):
        if carnum == k:
            continue
        if car == st.session_state[f"placement_{trackset}_{k}"]:
            st.session_state[f"placement_{trackset}_{k}"] = None
            return

def to_emoji(pos):
    row, col = pos
    padding = "   "
    return padding + emojis[row] + padding
    # return emojis[row] + " Race " + str(col + 1)

if not any(c is None for c in cars):
    for t in range(4):
        st.subheader(f"Trackset {t+1}")
        for row in range(5):
            st.pills(
                label="Select cars", options=[(row, col) for col in range(5)],
                selection_mode="multi", key=f"placement_{t}_{row}",
                label_visibility="collapsed", format_func=to_emoji,
            )
        # cols = st.columns(5)
        # for j, col in enumerate(cols):
        #     col.pills(
        #         label="Select cars", options=emojis, selection_mode="multi",
        #         key=f"placement_{i}_{j}", label_visibility="collapsed",
        #     )
            # car = col.selectbox(
            #     "Location", options=cars, index=None,
            #     key=f"placement_{i}_{j}", placeholder="Place car here",
            #     label_visibility="collapsed", on_change=swap_car, args=(i, j)
            # )
            # text = "❔" if car is None else emojis[cars.index(car)]
            # col.html(f"<h5 style='text-align: center'>{text}</h5>")
# TODO: Add "clear" buttons and status icons

def placements_valid() -> bool:
    # TODO: Add check for at least one value in column
    return all([
        all([
            st.session_state.get(f"placement_{t}_{row}", False)
            for row in range(5)
        ]) and True
        for t in range(4)
    ])

if placements_valid():
    placements = np.array([
        (t, row, pos[1])
        for t in range(4)
        for row in range(5)
        for pos in st.session_state[f"placement_{t}_{row}"]
    ])
    df = pd.DataFrame(placements, columns=["Trackset", "CarIdx", "Column"])

    # Average position within trackset
    df = df.groupby(["Trackset", "CarIdx"], sort=False, as_index=False).mean()[["CarIdx", "Column"]]

    # Average position overall
    df = df.groupby(["CarIdx"], sort=False, as_index=False).mean()

    # df["CarName"] = df["CarIdx"].apply(cars.__getitem__)
    # df["Emoji"] = df["CarIdx"].apply(emojis.__getitem__)
    # scores = list(zip(df["Column"], df["CarIdx"], df["Emoji"], df["CarName"]))
    scores = list(zip(df["Column"], df["CarIdx"]))
    scores.sort()

    st.divider()
    st.subheader("Best hand order")

    # Write separately to ensure row alignment
    cols = st.columns(5)
    for t, col in enumerate(cols):
        cont = col.container(height=68)
        cont.write(cars[scores[t][1]])
    cols = st.columns(5)
    for t, col in enumerate(cols):
        col.html(f"<h5 style='text-align: center;'>{emojis[scores[t][1]]}</h5>")
