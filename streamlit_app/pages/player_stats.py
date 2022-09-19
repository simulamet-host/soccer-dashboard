from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st

from arima_forecasting.arima_model import ArimaPlayerModel
from team_statistics.player_statistics import get_player_training_load_quantiles


def get_player_names(models: Dict[str, ArimaPlayerModel], team):
    return [(f"player{name[11:]}",name[:-4], name) for name in models.keys() if name[:5] == team]


def get_player(teams, player_name):
    all_players = {**teams["TeamA"].players, **teams["TeamB"].players}
    return all_players[player_name]


def player_statistics(teams, models):

    st.title("Player Statistics")
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

        forecast_step = st.slider("Forecasting Window", min_value=0, max_value=14)
        player_model = models[filter_player[2]]
        player = get_player(teams, filter_player[1])

    to_plot = player_model.y_train[-35:]
    if forecast_step > 0:
        forecast = player_model.predict(forecast_step)
        conf_interval = forecast.conf_int()
        to_plot = pd.concat([to_plot, forecast.predicted_mean])

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(20, 15))
    ax1.plot(to_plot)
    if forecast_step > 0:
        ax1.fill_between(conf_interval.index, conf_interval["lower readiness"],
                        conf_interval["upper readiness"], alpha=0.3)

    st.pyplot(fig)
    st.table(get_player_training_load_quantiles(player, 600, 21))