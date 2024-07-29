import streamlit as st

from components.injuries_objective import injuries_objective__common
from components.analysis import analysis_injuries_finn

def page_content():
    injuries_objective__common.page_setup()

    st.title('Injuries - Objective Data - Analysis')

    analysis_injuries_finn.view()

page_content()
