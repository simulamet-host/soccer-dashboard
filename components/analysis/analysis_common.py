import streamlit as st

from components.common import menu

def page_setup():
    st.set_page_config(
        page_title="Analysis - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # sidebar menu
    sub_pages = {
        'Game Performance': "pages/analysis_game_performance.py",
        'Illnesses': "pages/analysis_illnesses.py",
        "Injuries": "pages/analysis_injuries.py",
        'Training Load': "pages/analysis_training_load.py",
        'Wellness': "pages/analysis_wellness.py",
        'GPS': "pages/analysis_gps.py",
    }
    menu.menu(sub_pages, position=3)
