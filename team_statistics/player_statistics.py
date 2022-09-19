import pandas as pd

from preprocessing.data_loader import SoccerPlayer


def series_strip_nans(player: SoccerPlayer):
    first_idx = player.stress.first_valid_index()
    last_idx = player.stress.last_valid_index()
    return player.acwr.loc[first_idx:last_idx]


def get_player_training_load_quantiles(player: SoccerPlayer, quantile_time_scale, time_range):
    acwr = series_strip_nans(player)
    lower_quantile = acwr[:quantile_time_scale].quantile(.3)
    higher_quantile = acwr[:quantile_time_scale].quantile(.9)
    high_intensity = acwr[-time_range:].apply(lambda x: True if x >= higher_quantile else False).sum()
    low_intensity = acwr[-time_range:].apply(lambda x: True if x <= lower_quantile else False).sum()
    viz_series = acwr[-time_range:]
    #higher_quantile_vis = player.acwr[-time_range:].apply(lambda x: True if x <= lower_quantile else False)
    cols = ["indianred" if dat_point > higher_quantile else "skyblue" if
    dat_point < lower_quantile else "grey" for dat_point in viz_series]
    return viz_series, cols, pd.DataFrame([[low_intensity, high_intensity]],
                        columns=["Low Intensity Training Days", "High Intensity Training Days"])


def get_spider_plot_data(player: SoccerPlayer, time_range: int):
    return pd.DataFrame(dict(
        r=[player.mood[-time_range:].median(),
        player.stress[-time_range:].median(),
        player.fatigue[-time_range:].median(),
        player.soreness[-time_range:].median(),
        player.sleep_quality[-time_range:].median()],
        theta=["Mood",  "Stress", "Fatigue", "Soreness", "Sleep Quality"]))






