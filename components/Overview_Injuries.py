import streamlit as st

from utils import Data_fetcher

def overview_injuries():
    # fetch the data from the database
    table = 'injuries'
    columns = ['player_name', 'location', 'severity', 'date']
    df = Data_fetcher.fetch_data(table, columns)

    # summary statistics
    st.header('Summary statistics')
    st.write(df.describe())

    # first 5 rows of the dataset
    st.header('First 5 rows of the dataset')
    st.write(df.head())

    # bar chart for location
    st.header('Location of injuries')
    st.bar_chart(df['location'].value_counts())

    # bar chart for severity
    st.header('Severity of injuries')
    st.bar_chart(df['severity'].value_counts())
