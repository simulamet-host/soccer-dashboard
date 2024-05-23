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

        chart(new_df)

    # show the first row of each unique time value
    st.write('First row of each unique time value')
    st.dataframe(df, column_config={
        'lat': st.column_config.NumberColumn(format='%.7f'),
        'lon': st.column_config.NumberColumn(format='%.7f')
    })

def chart(new_df):
    # plot the raw lat and lon data
    fig, ax = plt.subplots()
    ax.plot(new_df['lon'], new_df['lat'], 'o-')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    # disable scientific notation
    ax.ticklabel_format(useOffset=False)
    # rotate the x-axis labels
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # plot on a football pitch
