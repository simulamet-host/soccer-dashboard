from pathlib import Path
import streamlit as st
import sys
import os
import pickle

# configuration of the page
st.set_page_config(
    page_title="Soccer Dashboard",# Title of the tab
    page_icon="⚽", # Icon of the tab
    layout="wide", # Content layout display
    initial_sidebar_state="auto", # Sidebar movement
    menu_items={
        'Get Help': 'https://www.simula.no',
        'Report a bug': "https://www.simula.no",
        'About': "Please read the README.md file for more informations about this Simula Research Lab project"
    }
) #  Top-right side of this app menu items

sys.path.append(str(Path(__file__).parent.parent))

from streamlit_app.page_functions.team_stats import team_statistics
from streamlit_app.page_functions.player_stats import player_statistics
from streamlit_app.page_functions.dataset_stats import dataset_statistics
from streamlit_app.page_functions.gps_stats import gps_statistics

path_to_teams = Path(__file__).parent.parent / "data" / "pickles" / "teams.pkl"
path_to_models = Path(__file__).parent.parent / "data" / "pickles" / "arima"

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

#@st.cache_data
#def load_in_gps(path_to_gps: Path):
    #gps = 
    #return gps.load(open(path_to_gps))

def get_player(teams, player_name):
    all_players = {**teams["TeamA"].players, **teams["TeamB"].players}
    return all_players[player_name]

# main page
def main_page(teams, models):
    with open('README.md', 'r') as file:
        descrip = file.read()
    descrip = str(descrip)
    index_1 = descrip.index('# Soccer Dashboard')
    index_2 = descrip.index('## ')
    st.markdown("## Welcome to the Soccer Dashboard")
    st.markdown(descrip[index_1:index_2])

path_to_teams = Path(__file__).parent.parent / "data" / "pickles" / "teams.pkl"
path_to_models = Path(__file__).parent.parent / "data" / "pickles" / "arima"
path_to_gps = Path(__file__).parent.parent / "data" / "gps" / "2020-06-01-TeamA-2d44f941.parquet"

models = load_in_arima_models(path_to_models)
teams = load_in_pickles(path_to_teams)
#statistics = load_in_pickles(path_to_stats)
#gps = load_in_gps(path_to_gps)

page_names_to_funcs = {
    "Homepage": main_page,
    "Dataset Statistics": dataset_statistics,
    "Player Information": player_statistics,
    "Team Information": team_statistics,
    "GPS Information": gps_statistics,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
if selected_page == "Homepage" or selected_page == "Player Information" or selected_page == "Team Information":
    page_names_to_funcs[selected_page](teams, models)
else:
    page_names_to_funcs[selected_page]()
