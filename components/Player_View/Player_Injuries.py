import altair as alt
import streamlit as st

from utils import Data_fetcher

def player_injuries():
    # fetch the data from the database
    table = 'injuries'
    columns = ['player_name', 'location', 'severity', 'date']
    df = Data_fetcher.fetch_data(table, columns)

    # add team column
    # team is the first part of the player_name
    df['team'] = df['player_name'].apply(lambda x: x.split('-')[0])

    # radio button to select the team
    team = st.radio('Select team', df['team'].unique(), horizontal=True)

    # dropdown to select the player
    player = st.selectbox('Select player', df[df['team'] == team]['player_name'].unique())

    # filter the data based on the selected team
    filtered_df = df[df['player_name'] == player]

    # show the filtered data
    bar_chart(filtered_df)

def bar_chart(df):
    # a horizontal stacked bar chart of location and severity
    st.header('Location and severity of injuries')

    chart = alt.Chart(df).mark_bar().encode(
        x='count()',
        y='location',
        color='severity',
        order=alt.Order(
            'severity',
            sort='descending'
        )
    ).transform_filter(
        # remove null values
        (alt.datum.location != 'null') & (alt.datum.severity != 'null')
    )

    st.altair_chart(chart, use_container_width=True)
