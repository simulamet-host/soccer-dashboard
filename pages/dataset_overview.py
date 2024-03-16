import streamlit as st

from components.common import menu
from components.dataset_overview import overview_injuries

def dataset_overview():
    st.set_page_config(
        page_title="Dataset Overview - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # sidebar menu
    sub_pages = {
        "Injuries": "pages/dataset_overview_injuries.py",
    }
    menu.menu(sub_pages)

    st.title('Dataset Overview')

    tab1, tab2 = st.tabs(['Injuries', 'Game Performance'])

    with tab1:
        overview_injuries.overview_injuries()

    with tab2:
        st.header('Game Performance')

dataset_overview()
