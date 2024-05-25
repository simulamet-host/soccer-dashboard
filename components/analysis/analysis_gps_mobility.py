import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
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
    ax.plot(df['x'], df['y'], 'o-', color='red', markersize=5)

    st.pyplot(fig)

    # plot a heatmap
    st.subheader('Heatmap')
    x = df['x'].dropna()
    y = df['y'].dropna()
    xy = np.vstack([x, y])
    # use gaussian kernel density estimation to calculate the density of the points
    z = gaussian_kde(xy)(xy)

    fig, ax = plt.subplots()
    # image of football pitch
    ax.imshow(image, extent=extent)
    # line to connect the points; set the zorder to ensure that it is below the dots; use the first color in the colormap
    ax.plot(x, y, '-', color=plt.cm.YlOrRd(0), zorder=1)
    # scatter plot with color based on the density
    ax.scatter(x, y, c=z, s=15, cmap='YlOrRd', zorder=2)
    st.pyplot(fig)
