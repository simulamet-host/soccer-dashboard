import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime

from src.utils.team_statistics_db import (
    get_average_metric_overview,
    get_correlation_matrix,
    get_feature_quantile_ts,
    get_injury_categories,
    get_std_metric_overview,
    convert_df
)


def team_statistics_db(teams, models):
    st.title("Team Information")
    tab1, = st.tabs(
        ["Training Load Overview"]
    )
    with st.sidebar:
        filter_team = st.radio(
            "Select Team",
            [("Team A", "TeamA"), ("Team B", "TeamB")],
            format_func=lambda x: x[0],
        )
    
    with tab1:
        st.subheader("Training Load Overview")
        moment = st.radio("Choose Statistic", ("Mean", "Standard Deviation"))


        if moment == "Mean":
            df = get_average_metric_overview(filter_team[1])
            st.table(
                df
            )
            csv = convert_df(df)
            st.download_button('📥"Press to Download"',
                               csv,
                               "training_load_overview_mean.csv",
                               "text/csv",
                               key='download-csv'
                               )

        else:
            df = get_std_metric_overview(filter_team[1])
            st.table(df)
            csv = convert_df(df)
            st.download_button('📥"Press to Download"',
                               csv,
                               "training_load_overview_std.csv",
                               "text/csv",
                               key='download-csv'
                               )