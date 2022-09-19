import pandas as pd

from preprocessing.data_loader import SoccerPlayer


def get_player_training_load_quantiles(player: SoccerPlayer, quantile_time_scale, time_range):
    lower_quantile = player.acwr[:-quantile_time_scale].quantile(.3)
    higher_quantile = player.acwr[:-quantile_time_scale].quantile(.8)
    high_intensity = player.acwr[-time_range:].apply(lambda x: True if x >= higher_quantile else False).sum()
    low_intensity = player.acwr[-time_range:].apply(lambda x: True if x <= lower_quantile else False).sum()
    return pd.DataFrame([[low_intensity, high_intensity]],
                        columns=["Low Intensity Training Days", "High Intensity Training Days"])





