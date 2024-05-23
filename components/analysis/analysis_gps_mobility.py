import matplotlib.pyplot as plt
import streamlit as st

from utils import data_fetcher
from utils import gps

def view():
    # fetch the data from the database
    table = 'gps'
    columns = ['*']
    df = data_fetcher.fetch_data(table, columns)

    # each time has many rows; we use the first row of each unique time value
    df = df.drop_duplicates(subset=['time'])

    # find unique player names
    players = df['player_name'].unique()

    for player in players:
        # the name of the player
        st.write(f'Mobility of the player *{player}*')

        # plot the lat and lon data of the player
        new_df = df[df['player_name'] == player]
        raw_chart(new_df)
        pitch_chart(new_df)

    # show the first row of each unique time value
    st.write('First row of each unique time value')
    st.dataframe(df, column_config={
        'lat': st.column_config.NumberColumn(format='%.7f'),
        'lon': st.column_config.NumberColumn(format='%.7f')
    })

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
    df['x'], df['y'], df['Pitch_length'], df['Pitch_width'], _ = zip(*df.apply(lambda row: gps.local_coordinates_for_point(row['lat'], row['lon']), axis=1))

    # image of football pitch, with offset
    image_path = 'assets/pitch.png'
    image = plt.imread(image_path)
    # todo: get the correct extent
    extent = [-3.4870576440713417, 108.09878696621159, -1.6914846756940938, 69.35087170345784]
    ax.imshow(image, extent=extent)

    # plot the points
    ax.plot(df['x'], df['y'], 'o-', color='red')

    st.pyplot(fig)

