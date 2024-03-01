import streamlit as st

from utils import Data_fetcher

def overview_injuries():
    st.write('This section will show the injuries of the players in the dataset')

    # fetch the data from the database
    table_name = 'injuries'
    columns = ['player_name', 'location', 'severity']
    df = Data_fetcher.fetch_from_mysql(table_name, columns)
