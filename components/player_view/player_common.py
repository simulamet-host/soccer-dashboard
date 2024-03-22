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
        "Injuries": "pages/player_view_injuries.py",
    }
    menu.menu(sub_pages, position=3)
