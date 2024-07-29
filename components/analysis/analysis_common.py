import streamlit as st

from components.common import menu

def page_setup():
    st.set_page_config(
        page_title="Analysis - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # sidebar menu
    menu.menu()
