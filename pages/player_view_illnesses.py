import streamlit as st

from components.player_view import player_common

def page_content():
    player_common.page_setup()

    st.title('Player View - Illnesses')

page_content()
