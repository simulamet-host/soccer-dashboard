import streamlit as st

from components.Player_View import Player_Injuries

def player_view():
    st.set_page_config(
        page_title="Player View - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.title('Player View')

    tab1, tab2 = st.tabs(['Injuries', 'Game Performance'])

    with tab1:
        Player_Injuries.player_injuries()

player_view()
