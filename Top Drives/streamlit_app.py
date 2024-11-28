import streamlit as st

pg = st.navigation([
    st.Page("challenge_solver.py", title="Challenge Solver", icon=":material/trophy:"),
    st.Page("flags.py", title="Flag Optimizer", icon=":material/sports_score:"),
    st.Page("placement_optimizer.py", title="Placement Optimizer", icon=":material/dashboard:")
])
st.set_page_config(page_title="Top Drives Assistant", page_icon=":material/laptop_car:")

pg.run()