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
    injury_df = gathered.groupby(["location", "severity"]).size().unstack(fill_value=0)
    #injury_df.index = ["Groin Hip", "Head Neck", "Left Foot", "Left Knee", "Left Leg",
    #                   "Left Thigh", "Right Foot", "Right Knee", "Right Leg", "Right Thigh",
    #                   "Stomach Back"]
    return injury_df


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
    "Mean ATL": [player.atl.mean().round(2) for player in players],
    "Mean ACWR" : [player.acwr.mean().round(2) for player in players],
    "Mean CTL28" : [player.ctl28.mean().round(2) for player in players],
    "Mean CTL42" : [player.ctl42.mean().round(2) for player in players],
    "Mean Strain" : [player.strain.mean().round(2) for player in players],
    "Mean Monotony" : [player.monotony.mean().round(2) for player in players],
    "Mean Daily Load" : [player.daily_load.mean().round(2) for player in players],
    "Mean Session RPE" : [np.round(np.nanmean(player.srpe), 2) for player in players]
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


def get_correlation_matrix(players: List[SoccerPlayer]):
    features = {"Daily Load":"daily_load", "sRPE":"srpe","RPE":"rpe", "Duration":"duration",
                "ATL":"atl", "Weekly Load": "weekly_load", "Monotony": "monotony", "Strain": "strain",
                "ACWR": "acwr", "CTL28": "ctl28", "CTL42": "ctl42", "Fatigue": "fatigue", "Mood": "mood",
                "Readiness": "readiness", "Sleep Duration": "sleep_duration", "Sleep Quality": "sleep_quality",
                "Soreness": "soreness", "Stress": "stress"}
    averaged_features = {}
    for feature_name, field_name in features.items():
        averaged_features[feature_name] = [np.nanmean(getattr(player, field_name)) for player in players]
    return pd.DataFrame(averaged_features).corr()


def convert_df(df):
   return df.to_csv().encode('utf-8')
