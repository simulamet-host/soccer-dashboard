import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime

from team_statistics.get_team_statistics import (
    get_average_metric_overview,
    get_correlation_matrix,
    get_feature_quantile_ts,
    get_injury_categories,
    get_std_metric_overview,
    convert_df
)


def team_statistics(teams, models):
    st.title("Team Information")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Aggregated Metrics", "Injury Overview", "Training Load Overview", "Correlation Analysis"]
    )
    with st.sidebar:
        filter_team = st.radio(
            "Select Team",
            [("Team A", "TeamA"), ("Team B", "TeamB")],
            format_func=lambda x: x[0],
        )
    with tab1:
        st.subheader("Aggregated Metrics")
        select_feature = st.selectbox(
            "Select Metric",
            [
                ("Readiness", "readiness"),
                ("Stress", "stress"),
                ("Mood", "mood"),
                ("Sleep Quality", "sleep_quality"),
                ("Sleep Duration", "sleep_duration"),
                ("Fatigue", "fatigue"),
                ("Soreness", "soreness"),
                ("ATL", "atl"),
                ("ACWR", "acwr"),
                ("Monotony", "monotony"),
                ("CTL28", "ctl28"),
                ("CTL42", "ctl42"),
                ("Strain", "strain"),
                ("Daily Load", "daily_load"),
                ("Weekly Load", "weekly_load"),
            ],
            format_func=lambda x: x[0],
        )
        feature_plot_data = get_feature_quantile_ts(
            teams[filter_team[1]].players.values(), select_feature[1]
        )
        date_range = st.slider(
            "Select Date Range",
            value=(
                feature_plot_data.index[0].to_pydatetime(),
                feature_plot_data.index[-1].to_pydatetime(),
            ),
            format="YYYY/MM/DD",
        )
        fig_feature, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 7))
        ax1.plot(
            feature_plot_data.index, feature_plot_data["median"], "o--", markersize=1
        )
        ax1.fill_between(
            feature_plot_data.index,
            feature_plot_data["lower_quantile"],
            feature_plot_data["higher_quantile"],
            alpha=0.5,
        )
        ax1.set_xlim(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Metric Value")
        st.pyplot(fig_feature)

    with tab2:
        st.subheader("Injury Overview")
        injuries = get_injury_categories(teams[filter_team[1]].players.values())
        sns.set_theme(style="darkgrid")
        fig_injuries, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 7))
        heatmap = sns.heatmap(
            ax=ax1, data=injuries.T, cmap="YlGnBu", annot=True, cbar=False, annot_kws={"fontsize": 17}
        )
        st.pyplot(fig_injuries)
    with tab3:
        st.subheader("Training Load Overview")
        moment = st.radio("Choose Statistic", ("Mean", "Standard Deviation"))


        if moment == "Mean":
            df = get_average_metric_overview(teams[filter_team[1]].players.values())
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
            df = get_std_metric_overview(teams[filter_team[1]].players.values())
            st.table(df)
            csv = convert_df(df)
            st.download_button('📥"Press to Download"',
                               csv,
                               "training_load_overview_std.csv",
                               "text/csv",
                               key='download-csv'
                               )

    with tab4:
        st.subheader("Correlation Analysis")
        sns.set_theme(style="darkgrid")
        correlation_matrix = get_correlation_matrix(teams[filter_team[1]].players.values())
        fig_corr, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 10))
        heatmap_corr = sns.heatmap(
            ax=ax1, data=correlation_matrix, cmap="YlOrBr", annot=True, cbar=True, annot_kws={"fontsize": 9}
        )
        st.pyplot(fig_corr)