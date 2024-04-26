import streamlit as st

from components.analysis import analysis_common

def analysis():
    analysis_common.page_setup()

    st.title('Analysis')

analysis()
