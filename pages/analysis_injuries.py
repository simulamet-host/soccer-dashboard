import streamlit as st

from components.analysis import analysis_common
from components.analysis import analysis_injuries

def page_content():
    analysis_common.page_setup()

    st.title('Analysis - Injuries')

    analysis_injuries.view()

page_content()
