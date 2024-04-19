import streamlit as st

from components.dataset_overview import overview_common
from components.dataset_overview import overview_wellness

def page_content():
    overview_common.page_setup()

    st.title('Dataset Overview - Wellness')

    overview_wellness.overview()

page_content()
