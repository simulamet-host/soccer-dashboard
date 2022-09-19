from typing import Dict, List
import json

import pandas as pd
import numpy as np

from preprocessing.data_loader import SoccerPlayer


def df_strip_nans(df: pd.DataFrame):
    first_idx = df.first_valid_index()
    last_idx = df.last_valid_index()
    return df.loc[first_idx:last_idx]


def get_injury_categories(players: List[SoccerPlayer]):
    injuries = [json.loads(item.type) for sublist in [player.injuries for player in players]
                 for item in sublist if json.loads(item.type)]
    processed_injuries = []
    for dicts in injuries:
        for key, value in dicts.items():
            processed_injuries.append((key, value))
    gathered = pd.DataFrame(processed_injuries, columns=["location", "severity"])
    return gathered.groupby(["location", "severity"]).size().unstack(fill_value=0)


def get_feature_quantile_ts(players: List[SoccerPlayer], feature):
    time_idx = list(players)[0].readiness.index
    nan_df = pd.DataFrame(np.array([getattr(player, feature) for player in players]).T, index=time_idx)
    feature_df = df_strip_nans(nan_df)
    median = feature_df.apply(lambda x: np.nanmedian(x), axis=1)
    lower_quantile = feature_df.apply(lambda x: np.nanquantile(x, 0.25), axis=1)
    higher_quantile = feature_df.apply(lambda x: np.nanquantile(x, 0.75), axis=1)
    return pd.DataFrame({"median": median, "lower_quantile": lower_quantile, "higher_quantile": higher_quantile},
                        index=feature_df.index)


def get_average_metric_overview(players: List[SoccerPlayer]):
    averages = {
    "μ ATL": [player.atl.mean().round(2) for player in players],
    "μ ACWR" : [player.acwr.mean().round(2) for player in players],
    "μ CTL28" : [player.ctl28.mean().round(2) for player in players],
    "μ CTL42" : [player.ctl42.mean().round(2) for player in players],
    "μ Strain" : [player.strain.mean().round(2) for player in players],
    "μ Monotony" : [player.monotony.mean().round(2) for player in players],
    "μ Daily Load" : [player.daily_load.mean().round(2) for player in players],
    "μ Session RPE" : [np.round(np.nanmean(player.srpe), 2) for player in players]
    }
    return pd.DataFrame(averages, index=[player.name[6:] for player in players])


def get_std_metric_overview(players: List[SoccerPlayer]):
    stds = {
    "STD ATL": [player.atl.std().round(2) for player in players],
    "STD ACWR" : [player.acwr.std().round(2) for player in players],
    "STD CTL28" : [player.ctl28.std().round(2) for player in players],
    "STD CTL42" : [player.ctl42.std().round(2) for player in players],
    "STD Strain" : [player.strain.std().round(2) for player in players],
    "STD Monotony" : [player.monotony.std().round(2) for player in players],
    "STD Daily Load" : [player.daily_load.std().round(2) for player in players],
    "STD Session RPE" : [np.round(np.nanstd(player.srpe), 2) for player in players]
    }
    return pd.DataFrame(stds, index=[player.name[6:] for player in players])


#def get_correlation_matrix(players: List[SoccerPlayer]):
#    features = ["daily_load", "srpe", "rpe", "duration", "atl", "weekly_load", "monotony", "strain", "acwr", "ctl28",
#                "ctl42", "fatigue", "mood", "readiness", "sleep_duration", "sleep_quality", "soreness", "stress"]



#TO DO:
# Implement readiness graph with range values, least ready most ready
# High exhaustion training days for team: last week and general -- daily load
# Team Mood: Weighted Average of Mood, Stress, Readiness
# Team Fatigue: Weighted Average of Sleep duration, Sleep quality, fatigue, ACWR
