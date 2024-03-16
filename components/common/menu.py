import streamlit as st

def menu():
    st.sidebar.page_link("homepage.py", label="Homepage")
    st.sidebar.page_link("pages/dataset_overview.py", label="Dataset Overview")
    st.sidebar.page_link("pages/player_view.py", label="Player View")
    st.sidebar.page_link("pages/team_view.py", label="Team View")
    st.sidebar.page_link("pages/researcher_view.py", label="Researcher View")
