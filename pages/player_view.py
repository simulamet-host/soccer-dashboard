import streamlit as st

from components.player_view import player_common
from components.player_view import player_injuries

def player_view():
    player_common.page_setup()

    st.title('Player View - Injuries')

    player_injuries.player_injuries()

player_view()
