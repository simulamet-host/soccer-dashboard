import streamlit as st

from components import Overview_Injuries

def dataset_overview():
    st.set_page_config(
        page_title="Dataset Overview - Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.title('Dataset Overview')

    tab1, tab2 = st.tabs(['Injuries', 'Game Performance'])

    with tab1:
        Overview_Injuries.overview_injuries()

    with tab2:
        st.header('Game Performance')

dataset_overview()
