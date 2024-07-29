import streamlit as st

from components.injuries_objective import injuries_objective__common

def page_content():
    injuries_objective__common.page_setup()

    st.title('Injuries - Objective Data - Overview')

page_content()
