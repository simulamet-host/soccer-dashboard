import altair as alt
import streamlit as st

from utils import data_fetcher

def overview():
    # fetch the data from the database
    table = 'game_performance'
    columns = ['*']
    df = data_fetcher.fetch_data(table, columns)

    # Number of records
    st.header('Number of records')
    # the number of records of the 3 metrics
    df_info = df.iloc[:, 2:5].count().reset_index()
    df_info.columns = ['Metric', 'Number of records']
    chart = alt.Chart(df_info).mark_bar().encode(
        x=alt.X('Metric', axis=alt.Axis(labelAngle=0, labelLimit=200), sort=None),
        y='Number of records'
    )
    st.altair_chart(chart, use_container_width=True)

    # the distribution of the 3 metrics
    st.header('Distribution of the 3 metrics')
    metric_columns = df.columns[2:5]
    for metric in metric_columns:
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(metric, bin=True),
            y='count()'
        )
        st.subheader(metric)
        st.altair_chart(chart, use_container_width=True)

    # summary statistics
    st.header('Summary statistics')
    st.write(df.describe())

    # first 5 rows of the dataset
    st.header('First 5 rows of the dataset')
    st.write(df.head())
