from pathlib import Path
import streamlit as st
import sys
import os
import pickle
sys.path.append(str(Path(__file__).parent.parent))

from streamlit_app.pages.team_stats import team_statistics
from streamlit_app.pages.player_stats import player_statistics

path_to_teams = Path(__file__).parent.parent / "data" / "pickles" / "teams.pkl"
path_to_models = Path(__file__).parent.parent / "data" / "pickles" / "arima"

st.set_page_config(layout="wide")
# configuration of the page


@st.cache
def load_in_pickles(path_to_data: Path):
    return pickle.load(open(path_to_data, "rb"))


@st.cache(allow_output_mutation=True)
def load_in_arima_models(path_to_arima: Path):
    all_files = os.listdir(path_to_arima)
    models = {}
    for file in all_files:
        models[file] = pickle.load(open(path_to_arima/file, "rb"))
    return models


models = load_in_arima_models(path_to_models)
teams = load_in_pickles(path_to_teams)


def main_page(teams, models):
    st.markdown("# Main page")
    st.markdown("")



page_names_to_funcs = {
    "Main Page": main_page,
    "Team Information": team_statistics,
    "Player Information": player_statistics,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page](teams, models)
