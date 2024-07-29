import streamlit as st

from components.dataset_overview import overview_common
from components.dataset_overview import overview_training_load

def page_content():
    overview_common.page_setup()

    st.title('Dataset Overview - Training Load')

    overview_training_load.overview()

page_content()
