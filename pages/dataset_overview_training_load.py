import streamlit as st

from components.dataset_overview import overview_common

def page_content():
    overview_common.page_setup()

    st.title('Dataset Overview - Training Load')

page_content()
