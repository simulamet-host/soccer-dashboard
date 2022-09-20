import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime

from team_statistics.get_team_statistics import (
    get_average_metric_overview,
    get_injury_categories,
    get_feature_quantile_ts,
    get_std_metric_overview,
)


def team_statistics(teams, models):
    st.title("Team Analysis")
    tab1, tab2, tab3 = st.tabs(
        ["Team Features", "Injury Overview", "Training Load Metrics"]
    )
    with st.sidebar:
        filter_team = st.radio(
            "Select Team",
            [("Team A", "TeamA"), ("Team B", "TeamB")],
            format_func=lambda x: x[0],
        )
    with tab1:
        select_feature = st.selectbox(
            "Select Feature",
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
            teams["TeamA"].players.values(), select_feature[1]
        )
        date_range = st.slider(
            "Select Date Range",
            value=(
                feature_plot_data.index[0].to_pydatetime(),
                feature_plot_data.index[-1].to_pydatetime(),
            ),
            format="MM/DD/YY",
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
        st.pyplot(fig_feature)

    with tab2:
        injuries = get_injury_categories(teams[filter_team[1]].players.values())
        font = {"family": "normal", "weight": "normal", "size": 17}
        sns.set_theme(style="darkgrid")
        fig_injuries, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 7))
        heatmap = sns.heatmap(
            ax=ax1, data=injuries.T, cmap="YlGnBu", annot=True, cbar=False
        )
        plt.rc("font", **font)
        st.pyplot(fig_injuries)
    with tab3:
        st.subheader("Table of Averaged Training Load Metrics")
        moment = st.radio("Choose Moment", ("Mean", "Standard Deviation"))
        if moment == "Mean":
            st.table(
                get_average_metric_overview(teams[filter_team[1]].players.values())
            )
        else:
            st.table(get_std_metric_overview(teams[filter_team[1]].players.values()))
