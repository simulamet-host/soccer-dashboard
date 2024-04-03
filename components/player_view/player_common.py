import streamlit as st

from components.common import menu

def page_setup():
    st.set_page_config(
        page_title="Player View - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # sidebar menu
    sub_pages = {
        'Game Performance': "pages/player_view_game_performance.py",
        'Illnesses': "pages/player_view_illnesses.py",
        "Injuries": "pages/player_view_injuries.py",
        'Training Load': "pages/player_view_training_load.py",
        'Wellness': "pages/player_view_wellness.py",
    }
    menu.menu(sub_pages, position=3)
