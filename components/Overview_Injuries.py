import streamlit as st

from utils import Data_fetcher

def overview_injuries():
    # fetch the data from the database
    table_name = 'injuries'
    columns = ['player_name', 'location', 'severity']
    df = Data_fetcher.fetch_from_mysql(table_name, columns)

    # bar chart for location
    st.header('Location of injuries')
    st.bar_chart(df['location'].value_counts())

    # bar chart for severity
    st.header('Severity of injuries')
    st.bar_chart(df['severity'].value_counts())
