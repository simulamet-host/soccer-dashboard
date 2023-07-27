import pandas as pd
import src.utils.queries as qu

conn = qu.conn

def get_average_metric_overview(filter):
    
    daily_features_query='SELECT player_name, atl, acwr, ctl28, ctl42, strain, monotony, daily_load FROM daily_features WHERE player_name like "'+filter+'%";'
    daily_features=pd.read_sql(daily_features_query, conn)
    daily_features_avg=daily_features.groupby('player_name').mean().round(2).reset_index()
    daily_features_avg.rename(columns = {'player_name':'Player','atl':'Mean ATL','acwr':'Mean ACWR','ctl28':'Mean CTL28','ctl42':'Mean CTL42','strain':'Mean Strain','monotony':'Mean Monotony','daily_load':'Mean Daily Load'}, inplace = True)
    
    # "Mean Session RPE" : 0

    return daily_features_avg

def get_std_metric_overview(filter):

    daily_features_query='SELECT player_name, atl, acwr, ctl28, ctl42, strain, monotony, daily_load FROM daily_features WHERE player_name like "'+filter+'%";'
    daily_features=pd.read_sql(daily_features_query, conn)
    daily_features_std=daily_features.groupby('player_name').std().round(2).reset_index()
    daily_features_std.rename(columns = {'player_name':'Player','atl':'STD ATL','acwr':'STD ACWR','ctl28':'STD CTL28','ctl42':'STD CTL42','strain':'STD Strain','monotony':'STD Monotony','daily_load':'STD Daily Load'}, inplace = True)
    
    # "STD Session RPE" : 0

    return daily_features_std

def convert_df(df):
   return df.to_csv().encode('utf-8')