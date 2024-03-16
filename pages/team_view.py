import streamlit as st

from components.common import menu

def team_view():
    st.set_page_config(
        page_title="Team View - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    menu.menu()

    st.title('Team View')

team_view()
