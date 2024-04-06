import streamlit as st

from components.player_view import player_common
from components.player_view import player_gps

def page_content():
    player_common.page_setup()

    st.title('Player View - GPS')

    player_gps.view()

page_content()
