import streamlit as st

from components.analysis import analysis_gps_mobility
from components.gps import gps__common

def page_content():
    gps__common.page_setup()

    st.title('GPS Analysis - Overall Mobility')

    analysis_gps_mobility.view()

page_content()
