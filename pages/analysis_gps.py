import streamlit as st

from components.analysis import analysis_common
from components.analysis import analysis_gps

def page_content():
    analysis_common.page_setup()

    st.title('Analysis - GPS')

    tab1, tab2, tab3 = st.tabs(['Sprint', 'Mobility', 'Formation'])

    with tab1:
        analysis_gps.view()

    with tab2:
        st.subheader('Mobility')

    with tab3:
        st.subheader('Formation')

page_content()
