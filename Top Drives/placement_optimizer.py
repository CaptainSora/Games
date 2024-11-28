import streamlit as st

cars = [None for _ in range(5)]
emojis = ["⭐", "🔴", "🟩", "🔷", "🩷"]

st.subheader("Your hand")
car_cols = st.columns(5)
for i, car_col in enumerate(car_cols):
    cars[i] = car_col.text_area(
        "Car Placement", value=None, height=68, key=f"car_input_{i}",
        placeholder=f"Car {i+1}", label_visibility="collapsed"
    )
    car_col.html(f"<h5 style='text-align: center;'>{emojis[i]}</h5>")

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

if not any(c is None for c in cars):
    for i in range(4):
        st.subheader(f"Trackset {i+1}")
        cols = st.columns(5)
        for j, col in enumerate(cols):
            car = col.selectbox(
                "Location", options=cars, index=None,
                key=f"placement_{i}_{j}", placeholder="Place car here",
                label_visibility="collapsed", on_change=swap_car, args=(i, j)
            )
            text = "❔" if car is None else emojis[cars.index(car)]
            col.html(f"<h5 style='text-align: center'>{text}</h5>")
    placements = [
        (st.session_state[f"placement_{i}_{j}"], j)
        for i in range(4)
        for j in range(5)
    ]
else:
    placements = [(None, None)]

if not any([car[0] is None for car in placements]):
    st.divider()
    st.subheader("Best hand order")
    score = [0 for _ in range(5)]
    for car in placements:
        score[cars.index(car[0])] += car[1]
    score = [(score[i], i, cars[i]) for i in range(5)]
    score.sort()
    # Write separately to ensure row alignment
    cols = st.columns(5)
    for i, col in enumerate(cols):
        cont = col.container(height=68)
        cont.write(score[i][2])
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.html(f"<h5 style='text-align: center;'>{emojis[score[i][1]]}</h5>")
