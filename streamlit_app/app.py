from typing import Dict, List, Tuple
from pathlib import Path
import streamlit as st
import sys
import pickle
sys.path.append(str(Path(__file__).parent.parent))

#from streamlit_app.pages.team_stats import
#from streamlit_app.pages.player_stats import


path_to_teams = Path(__file__).parent.parent / "data" / "pickles" / "teams.pkl"

st.set_page_config(layout="wide")
# configuration of the page


@st.cache
def load_in_pickles(path_to_data: Path):
    return pickle.load(open(path_to_data, "rb"))


teams = load_in_pickles(path_to_teams)


def main_page(teams):
    st.markdown("# Main page")


page_names_to_funcs = {
    "Main Page": main_page,
    "Team Information": team_stats,
    "Player Information": players_stats,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page](teams)
