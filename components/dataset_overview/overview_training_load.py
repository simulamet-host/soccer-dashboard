import streamlit as st

from utils import data_fetcher

def overview():
    # fetch the data from the database
    table = 'daily_features'
    columns = ['date', 'player_name', 'acwr', 'atl', 'ctl28', 'ctl42', 'daily_load', 'monotony', 'strain', 'weekly_load']
    df = data_fetcher.fetch_data(table, columns)

    # summary statistics
    st.header('Summary statistics')
    st.write(df.describe())

    # first 5 rows of the dataset
    st.header('First 5 rows of the dataset')
    st.write(df.head())
