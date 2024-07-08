import streamlit as st

from utils import data_fetcher

def view():
    # fetch the data from Google Cloud Storage
    file = 'host-tmp.appspot.com/soccer-dashboard-dev/Finn/TeamB_case_inj.csv'
    df = data_fetcher.read_gc_csv(file)

    # move the last column ('session') to the 3rd position
    last_col = df.pop('session')
    df.insert(2, 'session', last_col)

    # shorten the player_id: use the first 6 characters and last 4 characters
    df['player_id'] = df['player_id'].str[:6] + df['player_id'].str[-4:]

    # overview of the data
    with st.expander('Show overview of the data'):
        overview(df)

    # visualize the data
    visualize(df)

def overview(df):
    st.header('Overview of the data')

    # the first 5 rows
    st.subheader('First 5 rows')
    st.write(df.head())

    # number of rows and columns
    st.subheader('Number of rows and columns')
    st.write(f'Number of rows: {df.shape[0]}')
    st.write(f'Number of columns: {df.shape[1]}')

    # basic statistics
    st.subheader('Basic statistics')
    st.write(df.describe(include='all'))
    # explanation of the statistics
    if st.checkbox('Show explanation of the statistics'):
        st.write('''
        Categorical Columns:
          - count: The number of non-null entries.
          - unique: The number of unique values.
          - top: The most frequent value.
          - freq: The frequency of the most frequent value.

        Numerical Columns:
          - count: The number of non-null entries.
          - mean: The average value.
          - std: The standard deviation.
          - min: The minimum value.
          - 25%: The 25th percentile (first quartile).
          - 50%: The median (50th percentile or second quartile).
          - 75%: The 75th percentile (third quartile).
          - max: The maximum value.
        ''')

    # missing values
    st.subheader('Number of missing values in each column')
    st.write(df.isnull().sum())

def visualize(df):
    st.header('Visualization')

    vis_overview(df)
    vis_feature(df)
    vis_time(df)

def vis_overview(df):
    st.subheader('Overview of sessions')
    # x-axis is 'date', y-axis is 'player_id', plot dots for each 'session' and color by 'session'
    # overlay: read from column 'incident_type', if the content is 'Injury', show a red dot, otherwise show nothing
    spec = {
        'encoding': {
            'x': date_axis(),
            'y': {'field': 'player_id', 'type': 'nominal'},
            'tooltip': [
                {'field': 'date', 'type': 'temporal'},
                {'field': 'player_id', 'type': 'nominal'},
                {'field': 'session', 'type': 'nominal'},
                {'field': 'incident_type', 'type': 'nominal'},
            ],
        },
        # use independent color scales for the two layers
        'resolve': {'scale': {'color': 'independent'}},
        'layer': [
            {
                'mark': 'circle',
                'encoding': {
                    'color': {'field': 'session', 'type': 'nominal'},
                }
            },
            {
                'mark': 'circle',
                'encoding': {
                    'color': {
                        'field': 'incident_type', 'type': 'nominal',
                        'scale': {
                            'domain': ['Injury'],
                            'range': ['red'],
                        },
                    },
                }
            }
        ]
    }
    st.vega_lite_chart(df, spec, use_container_width=True)

def vis_feature(df):
    # visualization for a specific feature (column)
    st.subheader('Distribution of a feature for all players')

    # exclude columns that are not suitable for visualization
    exclude = ['date', 'player_id', 'session', 'time']
    features = [col for col in df.columns if col not in exclude]

    # select a feature to visualize
    # set the default feature to 'city'
    index = features.index('city') if 'city' in features else 0
    feature = st.selectbox('Select a feature to visualize', features, index=index)
    if feature:
        # histogram for numerical features
        if df[feature].dtype in ['int64', 'float64']:
            st.vega_lite_chart(df, {
                'mark': 'bar',
                'encoding': {
                    'x': {'field': feature, 'type': 'quantitative', 'bin': True},
                    'y': {'aggregate': 'count', 'type': 'quantitative'}
                }
            }, use_container_width=True)

            st.write(df[feature].describe())
        else:
            # bar chart for categorical features
            st.vega_lite_chart(df, {
                'mark': 'bar',
                'encoding': {
                    'x': {
                        'field': feature, 'type': 'nominal',
                        'axis': {'labelAngle': 0},
                    },
                    'y': {
                        'aggregate': 'count',
                        'type': 'quantitative',
                    },
                }
            }, use_container_width=True)

            st.write(df[feature].value_counts())

def vis_time(df):
    # time series plot showing how a feature changes over time for selected player(s)
    st.subheader('Feature over time for selected player(s)')

    # select player(s)
    players = df['player_id'].unique()
    player = st.multiselect('Select player(s)', players, players[0])

    # fetch the data of feature groups from Google Cloud Storage
    # use it to generate category and feature selection dropdowns
    file = 'host-tmp.appspot.com/soccer-dashboard-dev/Finn/feature_groups.json'
    feature_groups = data_fetcher.read_gc_file(file, input_format='json')

    # exclude columns that are not suitable for visualization
    exclude = ['date', 'player_id', 'time']
    for key in feature_groups:
        feature_groups[key] = [col for col in feature_groups[key] if col not in exclude]

    # select a category
    category = st.selectbox('Select a feature category', list(feature_groups.keys()))
    # select a feature
    feature = st.selectbox('Select a feature to visualize', feature_groups[category])

    # filter the data
    player_df = df[df['player_id'].isin(player)]

    # line chart for numerical features
    if player_df[feature].dtype in ['int64', 'float64']:
        main_layer = {
            'mark': {'type': 'line', 'point': True, 'tooltip': True},
            'encoding': {
                'x': date_axis(),
                'y': {'field': feature, 'type': 'quantitative'},
                'color': {
                    'field': 'player_id', 'type': 'nominal',
                    'scale': {
                        # colors from Streamlit's default palette, excluding red to avoid confusion with 'Injury'
                        'range': [
                            '#0068c9', # blue
                            '#83c9ff', # light blue
                            '#ff8700', # orange
                            '#ffe08e', # light orange
                            '#09ab3b', # green
                            '#7defa1', # light green
                            '#6d3fc0', # purple
                            '#c89dff', # light purple
                            '#555867', # dark grey
                        ],
                    },
                },
            }
        }
    else:
        # scatter plot for categorical features
        # hide null values
        main_layer = {
            'mark': 'point',
            'transform': [{'filter': 'datum.' + feature + ' != null'}],
            'encoding': {
                'x': date_axis(),
                'y': {'field': feature, 'type': 'nominal'},
                'color': {'field': 'player_id', 'type': 'nominal'},
                'size': {'value': 100},
            }
        }

    # overlay: read from column 'incident_type', if the content is 'Injury', show a vertical red line, otherwise show nothing
    injury_layer = {
        'mark': 'rule',
        'encoding': {
            'x': date_axis(),
            'color': {
                'field': 'incident_type', 'type': 'nominal',
                'scale': {
                    'domain': ['Injury'],
                    'range': ['red'],
                },
            },
            'size': {'value': 5},
            'tooltip': [
                {'field': 'date', 'type': 'temporal'},
                {'field': 'player_id', 'type': 'nominal'},
                {'field': 'incident_type', 'type': 'nominal'},
            ]
        },
    }
    # label for the vertical line; value is player_id
    label_injury_layer = {
        'mark': {
            'type': 'text',
            'tooltip': False,
        },
        'encoding': {
            'x': date_axis(),
            'y': {'value': 0},
            'text': {'field': 'player_id', 'type': 'nominal'},
            # only show the text when incident_type is 'Injury'
            'opacity': {
                'condition': {'test': 'datum.incident_type == "Injury"', 'value': 1},
                'value': 0
            },
        },
    }

    spec = {
        'resolve': {'scale': {'color': 'independent'}},
        'layer': [
            main_layer,
            injury_layer,
            label_injury_layer,
        ]
    }
    st.vega_lite_chart(player_df, spec, use_container_width=True)

def date_axis():
    # if the x axis is date, use the following configuration
    x = {
            'field': 'date', 'type': 'temporal',
            'axis': {
                # date format: Jan 1, 2020
                'format': '%b %d, %Y',
                'grid': True,
                'tickCount': {"interval": "month", "step": 3},
            },
        }

    return x
