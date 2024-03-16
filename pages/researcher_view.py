import streamlit as st

from components.common import menu

def researcher_view():
    st.set_page_config(
        page_title="Researcher View - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    menu.menu()

    st.title('Researcher View')

researcher_view()
