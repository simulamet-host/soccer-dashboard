import streamlit as st

from components.player_view import player_common
from components.player_view import player_injuries

def page_content():
    player_common.page_setup()

    st.title('Player View - Injuries')

    player_injuries.player_injuries()

page_content()
