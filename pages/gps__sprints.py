import streamlit as st

from components.analysis import analysis_gps_sprint
from components.gps import gps__common

def page_content():
    gps__common.page_setup()

    st.title('GPS Analysis - Sprints')

    analysis_gps_sprint.view()

page_content()
