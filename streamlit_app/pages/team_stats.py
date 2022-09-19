import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime

from team_statistics.get_team_statistics import get_average_metric_overview, get_injury_categories, get_readiness_quantile_ts


def team_statistics(teams, models):
    st.title("Team Analysis")
    readiness_plot_data = get_readiness_quantile_ts(teams["TeamA"].players.values())
    with st.sidebar:
        filter_team = st.radio(
            "Select Team",
            [("Team A", "TeamA"), ("Team B", "TeamB")],
            format_func=lambda x: x[0],
        )
        date_range = st.slider("Select Date Range", value=(readiness_plot_data.index[0].to_pydatetime(),
                                                           readiness_plot_data.index[-1].to_pydatetime()),
                               format="MM/DD/YY")
        injuries = get_injury_categories(teams[filter_team[1]].players.values())
    font = {'family': 'normal',
            'weight': 'normal',
            'size': 17}
    sns.set_theme(style="darkgrid")
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(20, 15))
    heatmap = sns.heatmap(ax=ax1, data=injuries.T, cmap="YlGnBu", annot=True, cbar=False)
    plt.rc('font', **font)
    ax2.plot(readiness_plot_data.index, readiness_plot_data["median"], 'o--', markersize=1)
    ax2.fill_between(readiness_plot_data.index, readiness_plot_data["lower_quantile"],
                     readiness_plot_data["higher_quantile"], alpha=0.5)
    ax2.set_xlim(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
    st.pyplot(fig)
    st.subheader("Table of Averaged Training Load Metrics")
    st.table(get_average_metric_overview(teams[filter_team[1]].players.values()))