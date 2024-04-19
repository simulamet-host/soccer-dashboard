import altair as alt
import pandas as pd
import streamlit as st

from utils import data_fetcher

def overview():
    # fetch the data from the database
    table = 'illnesses'
    columns = ['*']
    df = data_fetcher.fetch_data(table, columns)

    # Number of records
    # the number of total records and number of records where "problem" is not "null"
    st.header('Number of records')
    df_info = pd.DataFrame({
        'Type': ['Total records', 'Records where "problem" is not "null"'],
        'Number of records': [df.shape[0], df[df['problem'] != 'null'].shape[0]],
    })
    # bar chart of df_info
    chart = alt.Chart(df_info).mark_bar().encode(
        x=alt.X('Type', axis=alt.Axis(labelAngle=0, labelLimit=200), sort=None),
        y='Number of records'
    )
    st.altair_chart(chart, use_container_width=True)

    # bar chart of number of records by problem
    st.header('Number of records by problem (excluding null)')
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('problem', axis=alt.Axis(labelAngle=0)),
        y='count()'
    ).transform_filter(
        # remove null values
        (alt.datum.problem != 'null')
    )
    st.altair_chart(chart, use_container_width=True)

    # bar chart of number of records by player
    st.header('Number of records by player (excluding null)')
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('player_name', axis=alt.Axis(labelAngle=-45)),
        y='count()'
    ).transform_filter(
        # remove null values
        (alt.datum.player_name != 'null')
    )
    st.altair_chart(chart, use_container_width=True)

    # summary statistics
    st.header('Summary statistics')
    st.write(df.describe())

    # first 5 rows of the dataset
    st.header('First 5 rows of the dataset')
    st.write(df.head())
