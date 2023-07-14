from typing import Dict, List
import json

import pandas as pd
import numpy as np

from backend_functions.data_loader import SoccerPlayer

import mysql.connector

def init_connection():
    #return mysql.connector.connect(user='mpg_pmsys_dashboard', password='rlD8o-gLbAdZ',port = 3306,
     #                         host='mlab.no',
      #                        database='mpg_pmsys')


    connection =  mysql.connector.connect(user='mpg_pmsys_dashboard', password='rlD8o-gLbAdZ',host='mlab.no',database='mpg_pmsys')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        return connection
    else:
        print("Error: Failed to connect to the database")

def run_query(query):
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

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


def get_average_metric_overview(filter):
    
    rows = run_query('SELECT player_name, atl, acwr, ctl28, ctl42, strain, monotony, daily_load  from daily_features where player_name like "'+filter+'%";')
    player_names = np.unique([row[0] for row in rows])
    #print(player_names)
    player_features = []
    for player in player_names:
        list_atl = []
        list_acwr = []
        list_ctl28 = []
        list_ctl42 = []
        list_strain = []
        list_monotony = []
        list_daily_load = []
        for row in rows:
            if player == row[0]:
                list_atl.append(row[1])
                list_acwr.append(row[2])
                list_ctl28.append(row[3])
                list_ctl42.append(row[4])
                list_strain.append(row[5])
                list_monotony.append(row[6])
                list_daily_load.append(row[7])
        player_features.append([player,np.round(np.mean(list_atl), 2), np.round(np.mean(list_acwr), 2), np.round(np.mean(list_ctl28), 2), np.round(np.mean(list_ctl42), 2), np.round(np.mean(list_strain), 2), np.round(np.mean(list_monotony), 2), np.round(np.mean(list_daily_load), 2)])
    #print(player_features)
    averages = {
    "Mean ATL": [player[1] for player in player_features],
    "Mean ACWR" : [player[2] for player in player_features],
    "Mean CTL28" : [player[3] for player in player_features],
    "Mean CTL42" : [player[4] for player in player_features],
    "Mean Strain" : [player[5] for player in player_features],
    "Mean Monotony" : [player[6] for player in player_features],
    "Mean Daily Load" : [player[7] for player in player_features],
    "Mean Session RPE" : 0
    }
    return pd.DataFrame(averages, index=[player[0][6:] for player in player_features])


def get_std_metric_overview(filter):
    rows = run_query('SELECT player_name, atl, acwr, ctl28, ctl42, strain, monotony, daily_load  from daily_features where player_name like "'+filter+'%";')
    player_names = np.unique([row[0] for row in rows])
    #print(player_names)
    player_features = []
    for player in player_names:
        list_atl = []
        list_acwr = []
        list_ctl28 = []
        list_ctl42 = []
        list_strain = []
        list_monotony = []
        list_daily_load = []
        for row in rows:
            if player == row[0]:
                list_atl.append(row[1])
                list_acwr.append(row[2])
                list_ctl28.append(row[3])
                list_ctl42.append(row[4])
                list_strain.append(row[5])
                list_monotony.append(row[6])
                list_daily_load.append(row[7])
        player_features.append([player,np.round(np.std(list_atl), 2), np.round(np.std(list_acwr), 2), np.round(np.std(list_ctl28), 2), np.round(np.std(list_ctl42), 2), np.round(np.std(list_strain), 2), np.round(np.std(list_monotony), 2), np.round(np.std(list_daily_load), 2)])
    #print(player_features)
    averages = {
    "STD ATL": [player[1] for player in player_features],
    "STD ACWR" : [player[2] for player in player_features],
    "STD CTL28" : [player[3] for player in player_features],
    "STD CTL42" : [player[4] for player in player_features],
    "STD Strain" : [player[5] for player in player_features],
    "STD Monotony" : [player[6] for player in player_features],
    "STD Daily Load" : [player[7] for player in player_features],
    "STD Session RPE" : 0
    }
    return pd.DataFrame(averages, index=[player[0][6:] for player in player_features])


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
