import streamlit as st

from components.analysis import analysis_common

def page_content():
    analysis_common.page_setup()

    st.title('Analysis - Wellness')

page_content()
