import streamlit as st

from components.common import menu
from components.player_view import player_injuries

def player_view():
    st.set_page_config(
        page_title="Player View - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    menu.menu()

    st.title('Player View')

    tab1, tab2 = st.tabs(['Injuries', 'Game Performance'])

    with tab1:
        player_injuries.player_injuries()

player_view()
