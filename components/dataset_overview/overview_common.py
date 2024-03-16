import streamlit as st

from components.common import menu

def page_setup():
    st.set_page_config(
        page_title="Dataset Overview - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # sidebar menu
    sub_pages = {
        'Game Performance': "pages/dataset_overview_game_performance.py",
        'Illnesses': "pages/dataset_overview_illnesses.py",
        "Injuries": "pages/dataset_overview_injuries.py",
        'Training Load': "pages/dataset_overview_training_load.py",
        'Wellness': "pages/dataset_overview_wellness.py",
    }
    menu.menu(sub_pages, position=2)
