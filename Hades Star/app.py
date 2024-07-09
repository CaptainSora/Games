import streamlit as st
import numpy as np
import pandas as pd
from collections import namedtuple

st.title("DRS Mining Simulator")

# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=["a", "b", "c"])

# st.line_chart(chart_data)

# st.slider("test slider", 1, 15, None, 1)

# st.button("hit me")

# st.selectbox("box", list(range(1, 16)))

# st.sidebar.selectbox("sidebar box", ["ooh look at me", "stop looking at me"])

# left, right = st.sidebar.columns(2)
# left.selectbox("left sidebar box", ["click me!", "left"])
# right.selectbox("right sidebar box", ["click me!", "right"])

# with (expander := st.expander("Hide and seek")):
#     st.write("Inside the with block")
# expander.write("Outside the with block")

Module = namedtuple("Module", ["name", "path", "min", "max"])

if "Miner Level" not in st.session_state:
    st.session_state["Miner Level"] = 1

miner_img_paths = [f"Hades Star/Img/MS{x}.webp" for x in range(0, 8)]

module_inputs = [
    Module("Mining Boost", "MiningBoost", 0, 15),
    Module("Remote Mining", "RemoteMining", 0, 15),
    Module("Crunch", "Crunch", 0, 15),
    Module("Genesis", "Genesis", 0, 15),
    Module("Enrich", "Enrich", 0, 15),
    Module("Artifact Boost", "ArtifactBoost", 1, 15),
    Module("DRS Level", "RedStar", 7, 12),
    Module("Miner Level", "", 1, 7),
    Module("Miner Quantity", "MS6", 1, 4),
    Module("Target Number of Boosts", "ArtifactBoost", 1, 25)
]

def change_mod_levels():
    global miner_level
    miner_level = st.session_state["Miner Level"]

module_values = [None for _ in module_inputs]

modnum = 0

for _ in range(3):
    for col in st.columns(3, gap="medium"):
        with col:
            img, field = st.columns([1, 3], vertical_alignment="center")
            mod = module_inputs[modnum]
            with img:
                if mod.name == "Miner Level":
                    st.image(miner_img_paths[st.session_state["Miner Level"]])
                else:
                    st.image(f"Hades Star/Img/{mod.path}.webp")
            with field:
                module_values[modnum] = st.number_input(
                    mod.name, min_value=mod.min, max_value=mod.max, step=1, format="%d", key=mod.name, on_change=change_mod_levels)
        modnum += 1

_, middle, _ = st.columns([1, 2, 1], gap="small")
with middle:
    img, field = st.columns([1, 5], vertical_alignment="center")
    mod = module_inputs[-1]
    with img:
        st.image(f"Hades Star/Img/{mod.path}.webp")
    with field:
        module_values[modnum] = st.number_input(
            mod.name, min_value=mod.min, max_value=mod.max, step=1, format="%d", key=mod.name)

st.button("Simulate!")

st.warning("Warning: Crunch is currently unsupported by the mining simulation", icon="⚠️")