import streamlit as st

from components.analysis import analysis_common
from components.analysis import analysis_gps

def page_content():
    analysis_common.page_setup()

    st.title('Analysis - GPS')

    analysis_gps.view()

page_content()
