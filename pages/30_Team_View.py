import streamlit as st

def team_view():
    st.set_page_config(
        page_title="Team View - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.title('Team View')

team_view()
