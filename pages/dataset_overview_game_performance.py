import streamlit as st

from components.dataset_overview import overview_common
from components.dataset_overview import overview_game_performance

def page_content():
    overview_common.page_setup()

    st.title('Dataset Overview - Game Performance')

    overview_game_performance.overview()

page_content()
