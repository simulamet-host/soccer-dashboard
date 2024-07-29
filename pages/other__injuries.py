import streamlit as st

from components.dataset_overview import overview_common
from components.dataset_overview import overview_injuries
from components.analysis import analysis_injuries

def page_content():
    overview_common.page_setup()

    st.title('Dataset Overview - Injuries')

    overview_injuries.overview_injuries()

    st.title('Analysis - Injuries')

    analysis_injuries.view()

page_content()
