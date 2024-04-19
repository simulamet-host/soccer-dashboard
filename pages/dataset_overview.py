import streamlit as st

from components.dataset_overview import overview_common
from components.dataset_overview import overview_general

def page_content():
    overview_common.page_setup()

    st.title('Dataset Overview - General Overview')

    overview_general.overview()

page_content()
