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
    df, session = select_data()

    # each time may have many rows; we use the first row of each unique time value
    df = df.drop_duplicates(subset=['time'])
    # drop na values and reset the index
    df = df.dropna().reset_index(drop=True)
    # drop rows where lat or lon is 0
    df = df[(df['lat'] != 0) & (df['lon'] != 0)]

    # use only 5% of the data
    new_df = df.iloc[int(0.05 * len(df)):int(0.10 * len(df))]
    st.write('For performance reasons, only 5% of the data is shown')

    show_charts(new_df, method='utm', session=session)

    with st.expander('Original coordinates'):
        raw_chart(new_df)

def select_data():
    # the complete path of a file is like this: host-tmp.appspot.com/soccer-dashboard-dev/SoccerMon/Objective/TeamB/2020/2020-07/2020-07-04/2020-07-04-TeamB-2f23d7d5-2326-49ce-b9c8-5a6303f785c5.parquet
    path = 'host-tmp.appspot.com/soccer-dashboard-dev/SoccerMon/Objective/'
    # available files
    files = [
        '2020-07-04-TeamB-101fbccc-ded7-33e8-b421-eaeb534097ca.parquet',
        '2020-07-04-TeamB-247a8333-f7b0-b7d2-cda8-056c3d15eef7.parquet',
        '2020-07-10-TeamB-101fbccc-ded7-33e8-b421-eaeb534097ca.parquet',
        '2020-07-10-TeamB-2f23d7d5-2326-49ce-b9c8-5a6303f785c5.parquet',
    ]
    # select match date
    # find the unique dates from the file names with a fixed order
    dates = sorted(set([file[:10] for file in files]))
    date = st.selectbox('Select match date', dates)
    # select player
    # find files with the selected date, and the part after date and before .parquet is the player name, with a fixed order
    players = sorted(set([file[11:-8] for file in files if file[:10] == date]))
    player = st.selectbox('Select player', players)

    # extract path components from the selected date and player
    team = player.split('-')[0]
    year, month, _ = date.split('-')
    session = f'{date}-{player}'
    file = f'{path}{team}/{year}/{year}-{month}/{date}/{session}.parquet'

    df = data_fetcher.read_gc_file(file, input_format='parquet')

    return df, session

def show_charts(df, method, session):
    subheader = 'UTM' if method == 'utm' else method.capitalize()
    st.subheader(subheader)

    # convert the lat and lon data to x and y data
    result = gps.convert_coordinates(df['lat'], df['lon'], method=method)
    if result is None:
        st.write('Pitch not found')
        return
    coords, pitch = result

    # plot the rotated x and y data
    fig, ax = plt.subplots()

    # image of football pitch, with offset
    image_path = 'assets/pitch.png'
    image = plt.imread(image_path)
    extent = gps.pitch_image_extent(pitch['length'], pitch['width'])
    ax.imshow(image, extent=extent)

    # plot the dots
    ax.plot(*coords, 'o-', color='red', markersize=5)
    st.pyplot(fig)

    # heatmap and animation
    heatmap_chart(*coords, image, extent)
    load_animation(*coords, image, extent, session)

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

def load_animation(x, y, image, extent, session):
    # use 1 out of 5 points
    x = x[::5]
    y = y[::5]

    # read files from Google Cloud Storage
    conn = st.connection('gcs', type=FilesConnection)
    path = 'host-tmp.appspot.com/soccer-dashboard-dev/animations/'
    names = ['animation', 'step_animation']

    for name in names:
        subheader = 'Live playback' if name == 'animation' else 'Step animation'
        st.subheader(subheader)
        st.write('For performance reasons, only 1% of the data is shown')

        file = f'{path}{name}-{session}.html'
        # if the file exists, read and show the content; otherwise, create the file
        if conn._instance.exists(file):
            with conn.open(file, 'r') as f:
                ani_html = f.read()
        else:
            ani = animation_chart(x, y, image, extent) if name == 'animation' else step_animation_chart(x, y, image, extent)
            ani_html = ani.to_jshtml()
            # save the animation to a file
            with conn.open(file, 'w') as f:
                f.write(ani_html)

        components.html(ani_html, height=600)

def animation_chart(x, y, image, extent):
    # live playback/animation
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

def step_animation_chart(x, y, image, extent):
    # only show the last 3 points
    fig, ax = plt.subplots()
    ax.imshow(image, extent=extent)
    ln, = plt.plot([], [], 'ro')

    def update(i):
        ln.set_data(x[i:i+3], y[i:i+3])
        return ln,

    ani = FuncAnimation(fig, update, frames=range(len(x)), blit=True)

    return ani
