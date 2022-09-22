import pandas as pd

from preprocessing.data_loader import SoccerPlayer


def series_strip_nans(player: SoccerPlayer):
    first_idx = player.stress.first_valid_index()
    last_idx = player.stress.last_valid_index()
    return {"acwr": player.acwr.loc[first_idx:last_idx],
            "mood": player.mood.loc[first_idx:last_idx],
            "stress": player.stress.loc[first_idx:last_idx],
            "fatigue": player.fatigue.loc[first_idx:last_idx],
            "soreness": player.soreness.loc[first_idx:last_idx],
            "sleep_quality": player.sleep_quality.loc[first_idx:last_idx],}


def get_player_training_load_quantiles(player: SoccerPlayer, quantile_time_scale, time_range):
    acwr = series_strip_nans(player)["acwr"]
    lower_quantile = acwr[:quantile_time_scale].quantile(.25)
    higher_quantile = acwr[:quantile_time_scale].quantile(.75)
    high_intensity = acwr[-time_range:].apply(lambda x: True if x >= higher_quantile else False).sum()
    low_intensity = acwr[-time_range:].apply(lambda x: True if (x <= lower_quantile) and (x > 0) else False).sum()
    viz_series = acwr[-time_range:]
    cols = ["indianred" if dat_point > higher_quantile else "skyblue" if
    dat_point < lower_quantile else "grey" for dat_point in viz_series]
    return viz_series, cols, pd.DataFrame([[low_intensity, high_intensity]],
                        columns=["Low Training Load Days", "High Training Load Days"])


def get_spider_plot_data(player: SoccerPlayer, time_range: int):
    stipped_feats = series_strip_nans(player)
    return pd.DataFrame(dict(
        r=[stipped_feats["mood"][-time_range:].median(),
           stipped_feats["stress"][-time_range:].median(),
        stipped_feats["fatigue"][-time_range:].median(),
        stipped_feats["soreness"][-time_range:].median(),
        stipped_feats["sleep_quality"][-time_range:].median()],
        theta=["Mood",  "Stress", "Fatigue", "Soreness", "Sleep Quality"]))






