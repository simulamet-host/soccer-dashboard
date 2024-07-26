import streamlit as st

from components.analysis import analysis_common
from components.analysis import analysis_injuries_finn

def page_content():
    analysis_common.page_setup()

    st.title('Analysis - Injuries - Finn')

    analysis_injuries_finn.view()

page_content()
