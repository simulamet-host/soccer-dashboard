import streamlit as st

def player_view():
    st.set_page_config(
        page_title="Player View - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.title('Player View')

player_view()
