from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import streamlit as st
import streamlit.components.v1 as components
from st_files_connection import FilesConnection

from utils import data_fetcher
from utils import gps

def view():
    # select data table
    table = st.radio('Select data table', ['gps', 'gps_20200601'], horizontal=True)

    # fetch the data from the database
    columns = ['player_name', 'lat', 'lon', 'time']
    # because there are too many rows in table gps_20200601, we only take 1 row out of every 10 rows
    where = 'WHERE id % 10 = 0' if table == 'gps_20200601' else None
    df = data_fetcher.fetch_data(table, columns, limit=1000)

    # each time may have many rows; we use the first row of each unique time value
    df = df.drop_duplicates(subset=['time'])

    # drop na values and reset the index
    df = df.dropna().reset_index(drop=True)

    # find unique player names
    players = df['player_name'].unique()

    for player in players:
        # the name of the player
        st.write(f'Mobility of the player *{player}*')

        # plot the lat and lon data of the player
        new_df = df[df['player_name'] == player]

        new_chart(new_df)

        pitch_chart(new_df)

        with st.expander('Original coordinates'):
            raw_chart(new_df)

def new_chart(df):
    # new equirectangular projection
    st.subheader('Equirectangular projection')

    # use the first point to find the pitch
    pitch = gps.find_pitch(df.iloc[0]['lat'], df.iloc[0]['lon'])
    if pitch is None:
        st.write('Pitch not found')
        return
    angle = pitch['bearing']
    base_point = (pitch['lat'][0], pitch['lon'][0])
    base_x, base_y = gps.equirectangular(base_point[0], base_point[1])

    # use gps.equirectangular to convert the lat and lon to x and y
    df['x'], df['y'] = zip(*df.apply(lambda row: gps.equirectangular(row['lat'], row['lon']), axis=1))
    # x and y are relative to the base point
    df['x'] = df['x'] - base_x
    df['y'] = df['y'] - base_y

    # use gps.rotate_coordinates to rotate the coordinates
    df['rx'], df['ry'] = zip(*df.apply(lambda row: gps.rotate_coordinates(row['x'], row['y'], angle), axis=1))

    # plot the rotated x and y data
    fig, ax = plt.subplots()

    # image of football pitch, with offset
    image_path = 'assets/pitch.png'
    image = plt.imread(image_path)
    # todo: get the correct extent
    extent = [-3.4870576440713417, 108.09878696621159, -1.6914846756940938, 69.35087170345784]
    ax.imshow(image, extent=extent)

    # plot the dots
    ax.plot(df['rx'], df['ry'], 'o-', color='red', markersize=5)
    st.pyplot(fig)

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
    # use haversine
    st.subheader('Haversine')

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

    # drop na values and reset the index
    x = df['x'].dropna().reset_index(drop=True)
    y = df['y'].dropna().reset_index(drop=True)

    # plot the points
    ax.plot(x, y, 'o-', color='red', markersize=5)
    st.pyplot(fig)

    # heatmap and animation
    heatmap_chart(x, y, image, extent)
    load_animation(x, y, image, extent)

def heatmap_chart(x, y, image, extent):
    # plot a heatmap
    st.subheader('Heatmap')
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

def load_animation(x, y, image, extent):
    # if the file exists, read and show the content; otherwise, create the file
    conn = st.connection('gcs', type=FilesConnection)
    file_path = 'host-tmp.appspot.com/soccer-dashboard-dev/animations/animation.html'
    if conn._instance.exists(file_path):
        with conn.open(file_path, 'r') as file:
            ani_html = file.read()
    else:
        with conn.open(file_path, 'w') as file:
            ani = animation_chart(x, y, image, extent)
            ani_html = ani.to_jshtml()
            file.write(ani_html)

    components.html(ani_html, height=600)

def animation_chart(x, y, image, extent):
    # live playback/animation
    st.subheader('Live playback')
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.imshow(image, extent=extent)
        return ln,

    def update(frame):
        xdata.append(x[frame])
        ydata.append(y[frame])
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=range(len(x)), init_func=init, blit=True)

    return ani
