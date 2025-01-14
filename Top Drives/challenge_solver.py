from dataclasses import dataclass
from datetime import datetime as dt
from json import dumps, load
from itertools import combinations, permutations, product
from time import sleep

import streamlit as st


st.write("Challenge solver!")

st.session_state["cars"] = st.session_state.get("cars", {})
st.session_state["rounds"] = st.session_state.get("rounds", {})
st.session_state["set_rq"] = st.session_state.get("set_rq", False)
st.session_state["wins"] = st.session_state.get("wins", {})

@dataclass
class Car:
    name: str
    rq: int
    tune: str
    wild: bool

    def __repr__(self) -> str:
        return (
            f"rq{self.rq} {self.name} [{self.tune}]"
            f"{' (Wild)' if self.wild else ''}"
        )

with st.expander("Edit Cars", icon=":material/swap_driving_apps:"):
    # Add Car
    with st.form("add_car", clear_on_submit=True):
        rq, name, tune, wild = st.columns(
            [2, 8, 3, 2], vertical_alignment="bottom"
        )

        with rq:
            st.number_input(
                "RQ", min_value=10, max_value=119, value=None, step=1,
                label_visibility="hidden", placeholder="RQ", key="rq_input",
            )

        with name:
            st.text_input(
                "Name", label_visibility="hidden", placeholder="Car Name",
                key="name_input",
            )

        with tune:
            st.selectbox(
                "Tune", options=["332", "323", "233", "111", "000"],
                index=None, label_visibility="hidden", placeholder="Tune",
                key="tune_input",
            )

        with wild:
            st.toggle("Wild", key="wild_input",)
        
        if st.form_submit_button("Add car", type="primary"):
            if any(
                    st.session_state[f"{v}_input"] is None
                    for v in ["rq", "name", "tune", "wild"]
                ):
                st.error("At least one value is empty!")
            else:
                car = Car(
                    rq=st.session_state.rq_input,
                    name=st.session_state.name_input,
                    tune=st.session_state.tune_input,
                    wild=st.session_state.wild_input
                )
                if str(car) in st.session_state["cars"]:
                    st.error(f"{car} alredy exists!")
                else:
                    st.info(f"Added {car}")
                    st.session_state["cars"][str(car)] = car

    # Remove car
    with st.form("remove_car", clear_on_submit=True):
        st.selectbox(
            "Remove Car", options=st.session_state["cars"].values(),
            label_visibility="hidden", key="remove_car"
        )
        
        if st.form_submit_button("Remove car", type="primary"):
            if st.session_state["remove_car"] is None:
                st.error("Please select a car to remove!")
            else:
                car = st.session_state.remove_car
                st.info(f"Removed {car}")
                del st.session_state["cars"][str(car)]

    st.write(st.session_state["cars"].keys())

with st.expander("Edit Rounds", icon=":material/book_ribbon:"):
    with st.form("add_rounds", clear_on_submit=True):
        chapter, round_start, round_end = st.columns(3)

        with chapter:
            st.number_input(
                "chapter", min_value=1, max_value=12, value=None, step=1,
                label_visibility="hidden", placeholder="Chapter",
                key="chapter_input",
            )
        
        with round_start:
            st.number_input(
                "round_start", min_value=1, max_value=100, value=None, step=1,
                label_visibility="hidden", placeholder="Start",
                key="round_start_input",
            )

        with round_end:
            st.number_input(
                "round_end", min_value=1, max_value=100, value=None, step=1,
                label_visibility="hidden", placeholder="End",
                key="round_end_input",
            )

        chapter = st.session_state["chapter_input"]
        start = st.session_state["round_start_input"]
        end = st.session_state["round_end_input"]

        if st.form_submit_button("Add RQ limits", type="primary"):
            st.session_state["set_rq"] = False
            if any(v is None for v in [chapter, start, end]):
                st.error("Must complete all fields")
            elif start > end:
                st.error("Start round cannot be after end round!")
            else:
                st.session_state["set_rq"] = True
    
    if st.session_state["set_rq"]:
        with st.form("add_rq", clear_on_submit=True):
            width = 3
            entries = []
            while len(entries) < (end - start + 1):
                entries.extend(st.columns(width))
            for round in range(start, end + 1):
                col = entries[round - start]
                col.number_input(
                    f"{chapter}-{round}", min_value=50, max_value=500, value=None,
                    step=1, placeholder="RQ", key=f"{chapter}-{round}_input"
                )
            
            if st.form_submit_button("Submit rounds", type="primary"):
                if any(
                    st.session_state[f"{chapter}-{round}_input"] is None
                    for round in range(start, end + 1)
                ):
                    st.error("Every round must have a RQ limit!")
                else:
                    for round in range(start, end + 1):
                        st.session_state["rounds"][f"{chapter}-{round}"] = st.session_state[f"{chapter}-{round}_input"]
                    st.session_state["set_rq"] = False
                        
    st.write(st.session_state["rounds"])

with st.expander("Select Wins", icon=":material/fact_check:"):
    car = st.selectbox(
        "Select Car", options=st.session_state["cars"].values(),
        label_visibility="hidden", key="select_car",
    )

    if car is not None:
        # Create defaults
        st.session_state["wins"][str(car)] = st.session_state["wins"].get(
            str(car),
            {}
        )
        with st.form("add_wins", clear_on_submit=True):
            base_options = [f"Race {i+1}" for i in range(5)]

            def to_options(flags: list[bool]) -> list[str]:
                return [base_options[i] for i in range(5) if flags[i]]
            
            def to_flags(options: list[str]) -> list[bool]:
                return [base_options[i] in options for i in range(5)]
            
            # List rounds
            for round in st.session_state["rounds"]:
                st.pills(
                    round, options=base_options, selection_mode="multi",
                    default=to_options(
                        st.session_state["wins"][str(car)].get(round, [False]*5)
                    ),
                    key=f"round_{round}_pills"
                )
            
            if st.form_submit_button("Submit wins", type="primary"):
                for r in st.session_state["rounds"]:
                    st.session_state["wins"][str(car)][r] = to_flags(
                        st.session_state[f"round_{r}_pills"]
                    )
                st.info(f"Submitted wins for {car}")
                car = None
    
    st.json(st.session_state["wins"], expanded=1)

with st.expander("Data", icon=":material/analytics:"):
    @st.fragment
    def download_data():
        data = {
            "cars": st.session_state["cars"],
            "rounds": st.session_state["rounds"],
            "wins": st.session_state["wins"],
        }
        timestamp = dt.now().strftime("%Y-%m-%dT%H%M%S")
        st.download_button(
            "Download Data", dumps(data, default=vars), type="primary",
            file_name=f"Challenge_Data_{timestamp}.json",
            mime="application/json", key="download_data"
        )
    
    download_data()

    @st.fragment
    def upload_data():
        st.file_uploader(
            "Upload", type=["json"], key="upload",
        )
    
    with st.form("Upload Data"):
        upload_data()
        if st.form_submit_button("Load data to page", type="primary"):
            file = st.session_state["upload"]
            if file is not None:
                data = load(file)
                st.session_state["cars"] = {
                    k: Car(**v) for k, v in data["cars"].items()
                }
                st.session_state["rounds"] = data["rounds"]
                st.session_state["wins"] = data["wins"]
                st.info("Successfully loaded data! Refreshing...")
                sleep(2)
                st.rerun()

def old_solution(car_pool):
    solution = {}
    for round in st.session_state["rounds"]:
        clear = False
        # Filter cars which have at least one win
        viable = [c for c in car_pool if any(st.session_state["wins"][str(car)][round])]
        # Brute force test for wins
        for hand in permutations(viable, 5):
            total_rq = sum([car.rq for car in hand])
            if total_rq > st.session_state["rounds"][round]:
                continue
            clear = all([
                st.session_state["wins"][str(hand[j])][round]
                for j in range(len(hand))
            ])
            if clear:
                solution[round] = hand
                break
        else:
            return False
    return solution

def new_solution(car_pool):
    solution = {}
    for round in st.session_state["rounds"]:
        winners = []
        for i in range(5):
            race_winners = [
                car for car in car_pool
                if st.session_state["wins"][str(car)].get(round, [False]*5)[i]
            ]
            winners.append(race_winners)
        for candidate in product(*winners):
            # Check rq
            total_rq = sum([car.rq for car in candidate])
            if total_rq > st.session_state["rounds"][round]:
                continue
            # Check for duplicates
            if len(set([str(car) for car in candidate])) < 5:
                continue
            # Success
            solution[round] = candidate
            break
        else: # nobreak
            # No solution found
            return False
    return solution
        

with st.expander("Solver", icon=":material/calculate:"):
    st.session_state["all_solutions"] = st.session_state.get("all_solutions", {})
    if st.button("Calculate!", type="primary"):
        # Split cars by wild/not wild
        cars_wild = [
            v for v in st.session_state["cars"].values() if v.wild
        ]
        cars_restricted = [
            v for v in st.session_state["cars"].values() if not v.wild
        ]
        # Loop over # of cars
        # TEMP: start at 4
        for i in range(4, len(cars_restricted) + 1):
            # Must have at least 5 cars
            if len(cars_wild) + i < 5:
                continue
            # Store solutions
            all_solutions = {}

            st.write(f"Testing {i} restricted cars...")
            for selection in combinations(cars_restricted, i):
                car_pool = cars_wild + list(selection)
                solution = new_solution(car_pool)
                if solution:
                    all_solutions[
                        ", ".join([str(car) for car in selection])
                    ] = solution
            if all_solutions:
                st.session_state["all_solutions"] = all_solutions
                break
        else: # nobreak
            st.error("No solutions found...")
    if st.session_state["all_solutions"]:
        st.write("Found a solution!")
        st.write("Car summary:")
        sol_list = [
            k.split(", ")
            for k in st.session_state["all_solutions"]
        ]
        sol_dict = {
            k: "".join([
                "✅" if k in sol else "❌"
                for sol in sol_list
            ])
            for sol in sol_list
            for k in sol
        }
        for k in sorted(sol_dict.keys()):
            st.write(k, sol_dict[k])
        st.selectbox(
            "Choose Solution",
            options=st.session_state["all_solutions"].keys(),
            key="solution_picker",
        )
        st.write("Selected cars:")
        st.write(st.session_state["solution_picker"].split(", "))
        st.write(st.session_state["all_solutions"][st.session_state["solution_picker"]])

        @st.fragment
        def download_solutions():
            timestamp = dt.now().strftime("%Y-%m-%dT%H%M%S")
            st.download_button(
                "Download Solutions", dumps(st.session_state["all_solutions"], default=vars),
                type="primary",
                file_name=f"Challenge_Solutions_{timestamp}.json",
                mime="application/json", key="download_solutions"
            )
        
        download_solutions()
