__author__ = 'Finn Bartels'
__version__ = '1.0'

import os
import re
import timeit
import platform
import argparse
import pyarrow

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

print('Python version: ', platform.python_version())

# Functions for objective data


def raw_find_obj_files(dir_, team_name, file_type):
    """
    Finds all files of a certain type in the OBJECTIVE folder of a team.
    """
    start = timeit.default_timer()
    print('Start finding files...')
    target_dir = os.path.join(dir_, 'OBJECTIVE', team_name)

    if not os.path.exists(target_dir):
        raise ValueError("Team directory does not exist.")

    result_files = []

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file_type in file:
                result_files.append(os.path.join(root, file))

    print('...done finding files (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return result_files


def raw_rearrange_obj_df_columns(df):
    """
    Rearranges the columns of the OBJECTIVE dataframe.
    """
    start = timeit.default_timer()
    print('Start rearranging columns...')

    # df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df = df.sort_values(by=['date', 'team_id', 'player_id', 'time'])
    df = df.reset_index(drop=True)

    df = df[['player_name', 'team_id', 'player_id', 'date', 'time',
             'lat', 'lon', 'heart_rate', 'speed', 'inst_acc_impulse',
             'accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z',
             'hacc', 'hdop', 'signal_quality', 'num_satellites']]
    print('...done rearranging columns (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return df


def raw_load_obj_data(files):
    """
    Loads the OBJECTIVE data from the parquet files.
    """
    start = timeit.default_timer()
    print('Start loading files...')

    dfs = []
    team_pattern = r'Team(.)'
    id_pattern = r'(?:TeamA-|TeamB-|TeamC-|TeamD-|TeamE-)(.*?)(?:\.parquet)'

    for file in files:
        team_match = re.search(team_pattern, file)
        team_part = team_match.group(1)

        id_match = re.search(id_pattern, file)
        id_part = id_match.group(1)

        df = pd.read_parquet(file)

        df_path_split_string = file.split('/')
        df_path_date = df_path_split_string[-2]

        df['date'] = df_path_date
        df['team_id'] = team_part
        df['player_id'] = id_part

        dfs.append(df)
    final_df = pd.concat(dfs, ignore_index=True)
    final_df = raw_rearrange_obj_df_columns(final_df)

    print('...done loading files (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return final_df


def raw_plot_data(df, plot_attributes):
    """
    Plot the raw data of each column.
    """
    start = timeit.default_timer()
    print('Start plotting data...')

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(9, 9))
    axes = axes.flatten()

    for index, item in enumerate(plot_attributes):
        ax = axes[index]
        ax.hist(df[item], bins=20, color='blue', alpha=0.7)
        ax.set_title(item)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('../plots/raw_attributes.png', bbox_inches='tight')
    # plt.show()
    print('...done plotting data (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))


def raw_reduce_data_frame(
    df,
    min_lat, max_lat,
    min_lon, max_lon,
    min_speed, max_speed,
    min_heart_rate, max_heart_rate,
    max_hacc,
    max_hdop,
    min_signal_quality,
    min_num_satellites
):
    """
    Reduces the data frame to a certain area, speed, heart_rate and quality of measurement accuracy.
    """
    start = timeit.default_timer()
    print('Start reducing data frame...')

    df_raw_len = len(df)
    df = df[
        (df['lat'].between(min_lat, max_lat, inclusive='both')) &
        (df['lon'].between(min_lon, max_lon, inclusive='both')) &
        (df['speed'].between(min_speed, max_speed, inclusive='both')) &
        (df['heart_rate'].between(min_heart_rate, max_heart_rate, inclusive='both')) &
        (df['hacc'] <= max_hacc) &
        (df['hdop'] <= max_hdop) &
        (df['signal_quality'] >= min_signal_quality) &
        (df['num_satellites'] >= min_num_satellites)
    ]

    print('Reduced to %.2f%% of the original dataframe.' %
          (len(df)/df_raw_len*100))
    print('...done reducing data frame (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return df


def raw_save_obj_data(df, dir_REDUCED, team_name, file_type):
    """
    Saves the reduced data frame to a parquet file.
    """
    start = timeit.default_timer()
    dir_REDUCED = os.path.join(dir_REDUCED, 'OBJECTIVE')
    dir_save = '%s/%s_reduced.%s' % (dir_REDUCED, team_name, file_type)
    print('Start saving objective data to %s ...' % (dir_save))
    if not os.path.exists('%s' % (dir_REDUCED)):
        print('Create directory %s ...' % (dir_REDUCED))
        os.makedirs(dir_REDUCED)
    df.to_parquet(dir_save)
    # to_function_name = f'to_{file_type}'
    # to_function = getattr(df, to_function_name)

    file_size_bytes = os.path.getsize(dir_save)
    file_size_gb = file_size_bytes / (1024 ** 3)
    print('...done saving objective data (%s GB) (%s sec.).' %
          (file_size_gb, round(timeit.default_timer() - start, 0)))
    return df


def raw_obj_pipeline(team_name, dir_ORIGINAL, file_type_obj, dir_REDUCED):
    """
    Runs the entire raw objective pipeline.
    """
    start = timeit.default_timer()
    print('Start raw objective pipeline...')
    raw_obj_files = raw_find_obj_files(dir_=dir_ORIGINAL,
                                       team_name=team_name,
                                       file_type=file_type_obj)
    df_raw_obj = raw_load_obj_data(files=raw_obj_files)

    print("Raw size: ", df_raw_obj.shape[0])

    selected_plot_attributes = ['lat', 'lon', 'speed', 'heart_rate', 'hacc',
                                'hdop', 'signal_quality', 'num_satellites', 'inst_acc_impulse']
    raw_plot_data(df=df_raw_obj,
                  plot_attributes=selected_plot_attributes)

    # hacc: Values below 1 are considered military level (less than 0.5m error), values below 5 are good (less than 2m error), values of 7 are almost unusable.
    # hdop: 1-2 Excellent At this confidence level, positional measurements are considered accurate enough to meet all but the most sensitive applications.
    #       2-5 Good Represents a level that marks the minimum appropriate for making accurate decisions. Positional measurements could be used to make reliable in-route navigation suggestions to the user.
    #       5-10 Moderate Positional measurements could be used for calculations, but the fix quality could still be improved. A more open view of the sky is recommended.
    #       10-20 Fair Represents a low confidence level. Positional measurements should be discarded or used only to indicate a very rough estimate of the current location.
    #       >20 Poor At this level, measurements are inaccurate by as much as 300 meters with a 6-meter accurate device (50 DOP × 6 meters) and should be discarded.
    df_reduced_obj = raw_reduce_data_frame(
        df=df_raw_obj,
        min_lat=0, max_lat=60,
        min_lon=0, max_lon=60,
        min_speed=0, max_speed=15,
        min_heart_rate=df_raw_obj['heart_rate'].min(), max_heart_rate=df_raw_obj['heart_rate'].max(),
        max_hacc=3,  # Thresholds: #Lars: 3
        max_hdop=10,  # Thresholds: #Lars: 10
        min_signal_quality=100,  # Thresholds: #Lars: 100
        min_num_satellites=4
    )

    df_reduced_obj = raw_save_obj_data(df=df_reduced_obj,
                                       dir_REDUCED=dir_REDUCED,
                                       team_name=team_name,
                                       file_type=file_type_obj)
    print('...done raw objective pipeline.')
    print('Runtime elapsed: %s sec.' %
          (round(timeit.default_timer() - start, 0)))
    return df_reduced_obj


# Functions for subjective data


def raw_find_subj_files(dir_, team_name, file_type):
    """
    Finds all files of a certain type in the SUBJECTIVE folder of a team.
    """
    start = timeit.default_timer()
    print('Start finding files...')
    target_dir = os.path.join(dir_, 'SUBJECTIVE/per player', team_name)
    print(target_dir)

    if not os.path.exists(target_dir):
        raise ValueError("Team directory does not exist.")

    result_files = []

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file_type in file:
                result_files.append(os.path.join(root, file))

    print('...done finding files (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return result_files


def raw_resettle_subj_df_columns(df):
    """
    Resettles previous index columns of the subjective dataframes.
    """
    start = timeit.default_timer()
    print('Start resettling the columns...')

    for df_by_feature in df:
        df_by_feature.columns = df_by_feature.columns.str.lower()
        if ('unnamed: 0' in df_by_feature.columns) and ('timestamp' in df_by_feature.columns):
            df_by_feature.drop(columns=['unnamed: 0'], inplace=True)
            df_by_feature.rename(columns={'timestamp': 'date'}, inplace=True)
        if 'unnamed: 0' in df_by_feature.columns:
            df_by_feature.rename(columns={'unnamed: 0': 'date'}, inplace=True)

    print('...done resettling columns (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return df


def raw_rearrange_subj_df_columns(df):
    """
    Returns a rearranged dataframe.
    """
    start = timeit.default_timer()
    print('Start rearranging columns...')

    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df = df.sort_values(by=['date', 'team_id', 'player_id'])
    df = df.reset_index(drop=True)

    df = df[['date', 'team_id', 'player_id', 'daily_load', 'atl', 'weekly_load',
             'monotony', 'strain', 'acwr', 'ctl28', 'ctl42', 'fatigue',
             'mood', 'readiness', 'sleep-duration', 'sleep-quality', 'soreness',
             'stress', 'injury_ts', 'team_performance', 'offensive_performance',
             'defensive_performance', 'problems', 'type', 'srpe', 'rpe', 'duration']]
    print('...done rearranging columns (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return df


def raw_load_subj_data(features, files):
    """
    Loads the SUBJECTIVE data from the csv files.
    """
    start = timeit.default_timer()
    print('Start loading files...')

    team_pattern = r'Team(.)'
    id_pattern = r'(?:TeamA-|TeamB-|TeamC-|TeamD-|TeamE-)(.*?)(?:\.csv)'

    df_names = 'df_'
    dfs_by_feature = []

    for feature in features:
        df_name = df_names + feature
        dfs = []
        for file in files:
            if feature in file:
                team_match = re.search(team_pattern, file)
                team_part = team_match.group(1)

                id_match = re.search(id_pattern, file)
                id_part = id_match.group(1)

                df = pd.read_csv(file)

                df_path_split_string = file.split('/')
                df_path_date = df_path_split_string[-2]

                # df['date'] = df_path_date
                df['team_id'] = team_part
                df['player_id'] = id_part

                df.drop(columns=['player_name'], inplace=True)

                dfs.append(df)
        globals()[df_name] = pd.concat(dfs, ignore_index=True)
        dfs_by_feature.append(globals()[df_name])

    dfs_by_feature = raw_resettle_subj_df_columns(df=dfs_by_feature)

    final_df = dfs_by_feature[0]
    for df_ in dfs_by_feature[1:]:
        final_df = pd.merge(final_df, df_, on=[
                            'date', 'team_id', 'player_id'], how='outer')

    final_df = raw_rearrange_subj_df_columns(final_df)

    print('...done loading files (%s sec.).' %
          (round(timeit.default_timer() - start, 0)))
    return final_df


def raw_save_subj_data(df, dir_REDUCED, team_name, file_type):
    """
    Saves the reduced data frame to a csv file.
    """
    start = timeit.default_timer()
    dir_REDUCED = os.path.join(dir_REDUCED, 'SUBJECTIVE')
    dir_save = '%s/%s_reduced.%s' % (dir_REDUCED, team_name, file_type)
    print('Start saving subjective data to %s ...' % (dir_save))
    if not os.path.exists('%s' % (dir_REDUCED)):
        print('Create directory %s ...' % (dir_REDUCED))
        os.makedirs(dir_REDUCED)
    df.to_csv(dir_save)
    # to_function_name = f'to_{file_type}'
    # to_function = getattr(df, to_function_name)

    file_size_bytes = os.path.getsize(dir_save)
    file_size_gb = file_size_bytes / (1024 ** 3)
    print('...done saving subjective data (%s GB) (%s sec.).' %
          (file_size_gb, round(timeit.default_timer() - start, 0)))
    return df


def raw_subj_pipeline(team_name, dir_ORIGINAL, file_type_subj, dir_REDUCED):
    """
    Runs the entire raw subjective pipeline.
    """
    start = timeit.default_timer()
    print('Start raw subjective pipeline...')

    raw_subj_files = raw_find_subj_files(dir_=dir_ORIGINAL,
                                         team_name=team_name,
                                         file_type=file_type_subj)
    df_raw_subj = raw_load_subj_data(features=['daily-features',
                                               'game-performance',
                                               'illness',
                                               'injuries',
                                               'session-features'
                                               ],
                                     files=raw_subj_files)
    df_reduced_subj = raw_save_subj_data(df=df_raw_subj,
                                         dir_REDUCED=dir_REDUCED,
                                         team_name=team_name,
                                         file_type=file_type_subj)

    print('...done raw subjective pipeline.')
    print('Runtime elapsed: %s sec.' %
          (round(timeit.default_timer() - start, 0)))
    return df_reduced_subj


def parse_args():
    '''
    '''
    parser = argparse.ArgumentParser(
        description='Parse arguments defining team and data information')
    parser.add_argument('--team_name', type=str,
                        choices=['TeamA', 'TeamB'], help='Choose the Team name.')
    parser.add_argument('--data', type=str, choices=[
                        'obj', 'subj', 'all'], help='Choose between objective and subjective data or all.')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    '''
    Prompt example: python3 pipeline_raw.py --team_name TeamA --data all
    '''
    args = parse_args()

    team_name = args.team_name
    dir_ORIGINAL = '../data/SoccerMon'
    file_type_obj = 'parquet'
    file_type_subj = 'csv'
    dir_REDUCED = '../data/SoccerMon_reduced'

    if args.data == 'obj':
        df_obj_reduced = raw_obj_pipeline(team_name=team_name,
                                          dir_ORIGINAL=dir_ORIGINAL,
                                          file_type_obj=file_type_obj,
                                          dir_REDUCED=dir_REDUCED
                                          )
    elif args.data == 'subj':
        df_subj_reduced = raw_subj_pipeline(team_name=team_name,
                                            dir_ORIGINAL=dir_ORIGINAL,
                                            file_type_subj=file_type_subj,
                                            dir_REDUCED=dir_REDUCED
                                            )
    elif args.data == 'all':
        df_obj_reduced = raw_obj_pipeline(team_name=team_name,
                                          dir_ORIGINAL=dir_ORIGINAL,
                                          file_type_obj=file_type_obj,
                                          dir_REDUCED=dir_REDUCED
                                          )
        df_subj_reduced = raw_subj_pipeline(team_name=team_name,
                                            dir_ORIGINAL=dir_ORIGINAL,
                                            file_type_subj=file_type_subj,
                                            dir_REDUCED=dir_REDUCED
                                            )
