from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.lines import Line2D
import plotly.express as px
import streamlit as st

from arima_forecasting.arima_model import ArimaPlayerModel
from team_statistics.player_statistics import (
    get_player_training_load_quantiles,
    get_spider_plot_data,
)


def get_player_names(models: Dict[str, ArimaPlayerModel], team):
    return [
        (f"player{name[11:]}", name[:-4], name)
        for name in models.keys()
        if name[:5] == team
    ]


def get_player(teams, player_name):
    all_players = {**teams["TeamA"].players, **teams["TeamB"].players}
    return all_players[player_name]


def player_statistics(teams, models):

    st.title("Player Information")
    tab1, tab2, tab3 = st.tabs(
        ["Readiness Forecast", "Wellness Overview", "Training Load Overview"]
    )
    with st.sidebar:
        filter_team = st.selectbox(
            "Select Team",
            [("Team A", "TeamA"), ("Team B", "TeamB")],
            format_func=lambda x: x[0],
        )
        player_names = get_player_names(models, filter_team[1])
        filter_player = st.selectbox(
            "Select Player",
            player_names,
            format_func=lambda x: x[0],
        )
    with tab1:
        st.subheader("Readiness Forecast")
        forecast_step = st.slider("Forecasting Window", min_value=0, max_value=14)
        player_model = models[filter_player[2]]
        to_plot = player_model.y_train[-35:]
        if forecast_step > 0:
            forecast = player_model.predict(forecast_step)
            conf_interval = forecast.conf_int()
            to_plot = pd.concat([to_plot, forecast.predicted_mean])

        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 7))
        ax1.plot(to_plot)
        ax1.tick_params(axis="x", labelrotation=45)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Readiness")
        if forecast_step > 0:
            ax1.fill_between(
                conf_interval.index,
                conf_interval["lower readiness"],
                conf_interval["upper readiness"],
                alpha=0.3,
            )

        st.pyplot(fig)

    with tab2:
        st.subheader("Wellness Parameter")
        player = get_player(teams, filter_player[1])
        wellness_parameter_window = st.radio(
            "Select Time Range ",
            (
                ("Last Week", 7),
                ("Last Fortnight", 14),
                ("Last Month", 30),
                ("Last Year", 365),
            ),
            format_func=lambda x: x[0],
        )
        spider_plot_df = get_spider_plot_data(player, wellness_parameter_window[1])
        fig_spider = px.line_polar(
            spider_plot_df, r="r", theta="theta", line_close=True, range_r=[0, 5], width=800, height=400)
        fig_spider.update_traces(fill="toself")
        st.plotly_chart(fig_spider)

    with tab3:
        st.subheader("Training Load Overview")
        intensity_time_range = st.radio(
            "Select Time Range",
            (
                ("Last Week", 7),
                ("Last Fortnight", 14),
                ("Last Month", 30),
                ("Last Year", 365),
            ),
            format_func=lambda x: x[0],
        )
        player = get_player(teams, filter_player[1])
        (
            acwr_visualisation,
            quantiles_viz,
            table_content,
        ) = get_player_training_load_quantiles(player, 650, intensity_time_range[1])

        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """

        # Inject CSS with Markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        st.table(table_content)
        fig_intensity, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(14, 7))
        ax1.bar(acwr_visualisation.index, acwr_visualisation, color=quantiles_viz)
        ax1.tick_params(axis="x", labelrotation=45)
        legend_elements = [Line2D([0], [0], color='indianred', lw=4, label='High Training Load Days'),
                           Line2D([0], [0], color='skyblue', lw=4, label='Low Training Load Days'),
                            Line2D([0], [0], color='grey', lw=4, label='Normal Training Load Days')]
        ax1.legend(handles=legend_elements)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Acute Chronic Work Load Ratio")
        st.pyplot(fig_intensity)
