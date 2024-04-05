import altair as alt
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

    bar_chart(df)

    time_series_chart(df)

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

def time_series_chart(df):
    # location of injuries over time
    st.header('Location of injuries over time')

    chart = alt.Chart(df).mark_circle().encode(
        x='yearmonth(date):T',
        y='location',
        size='count()'
    ).transform_filter(
        # remove null values
        (alt.datum.location != 'null') & (alt.datum.severity != 'null')
    )

    st.altair_chart(chart, use_container_width=True)
