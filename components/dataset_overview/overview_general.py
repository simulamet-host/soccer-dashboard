import pandas as pd
import streamlit as st

from utils import data_fetcher

def overview():
    # fetch the data from the database
    # use the daily_features table for now as it covers the most wide range
    table = 'daily_features'
    columns = ['*']
    df = data_fetcher.fetch_data(table, columns)

    st.write('The entire dataset contains:')

    # number of unique teams
    # team is the first part of the player_name
    df['team'] = df['player_name'].apply(lambda x: x.split('-')[0])
    num_teams = df['team'].nunique()
    st.write(f'**{num_teams}** unique teams:')
    st.write(df['team'].unique())

    # number of unique players
    num_players = df['player_name'].nunique()
    st.write(f'**{num_players}** unique players:')
    st.write(df['player_name'].unique())

    # number of unique years
    df['year'] = pd.DatetimeIndex(df['date']).year
    num_years = df['year'].nunique()
    st.write(f'**{num_years}** unique years:')
    # the years are displayed with a thousand separator by default, e.g., 2,020, so we remove the separator
    unique_years = pd.DataFrame(df['year'].unique(), columns=['value'])
    styled_unique_years = unique_years.style.format('{:.0f}')
    st.dataframe(styled_unique_years, hide_index=True)
