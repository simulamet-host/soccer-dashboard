import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from utils import data_fetcher
from utils import gps

def view():
    # select data table
    table = st.radio('Select data table', ['gps', 'gps_20200601'], horizontal=True)

    # fetch the data from the database
    columns = ['player_name', 'lat', 'lon', 'time']
    # because there are too many rows in table gps_20200601, we only take 1 row out of every 10 rows
    where = 'WHERE id % 10 = 0' if table == 'gps_20200601' else None
    df = data_fetcher.fetch_data(table, columns, where=where)

    # each time may have many rows; we use the first row of each unique time value
    df = df.drop_duplicates(subset=['time'])

    # find unique player names
    players = df['player_name'].unique()

    for player in players:
        # the name of the player
        st.write(f'Mobility of the player *{player}*')

        # plot the lat and lon data of the player
        new_df = df[df['player_name'] == player]
        with st.expander('Raw data'):
            raw_chart(new_df)

        pitch_chart(new_df)

def raw_chart(df):
    # plot the raw lat and lon data
    fig, ax = plt.subplots()
    ax.plot(df['lon'], df['lat'], 'o-', color='red')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    # disable scientific notation
    ax.ticklabel_format(useOffset=False)
    # rotate the x-axis labels
    plt.xticks(rotation=45)
    st.pyplot(fig)

def pitch_chart(df):
    # plot on a football pitch
    fig, ax = plt.subplots()

    # local coordinates
    df['x'], df['y'], df['Pitch_width'], df['Pitch_length'], _ = zip(*df.apply(lambda row: gps.local_coordinates_for_point(row['lat'], row['lon']), axis=1))

    # image of football pitch, with offset
    image_path = 'assets/pitch.png'
    image = plt.imread(image_path)
    # todo: get the correct extent
    extent = [-3.4870576440713417, 108.09878696621159, -1.6914846756940938, 69.35087170345784]
    ax.imshow(image, extent=extent)

    # plot the points
    ax.plot(df['x'], df['y'], 'o-', color='red')

    st.pyplot(fig)

    # plot a heatmap
    st.subheader('Heatmap')
    # the number of bins in x and y directions
    n_bins = (100, 60)
    # count the number of points in each bin
    mesh, x_edges, y_edges = np.histogram2d(df['x'], df['y'], bins=n_bins, range=[[0, df['Pitch_length'].max()], [0, df['Pitch_width'].max()]])
    # plot the heatmap on the football pitch
    fig, ax = plt.subplots()
    ax.imshow(image, extent=extent)
    # we want the lowest value to be transparent so that the football pitch is visible
    mesh[mesh == 0] = np.nan
    ax.imshow(mesh.T, cmap='YlOrRd', extent=extent, origin='lower', norm=plt.Normalize(vmin=0, vmax=10))
    st.pyplot(fig)
