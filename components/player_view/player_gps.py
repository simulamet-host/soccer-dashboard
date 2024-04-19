import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st

from utils import data_fetcher
from utils import gps

def view():
    # fetch the data from the database
    table = 'LH_HIR'
    columns = ['*']
    df = data_fetcher.fetch_data(table, columns)

    # radio button to select the team
    team = st.radio('Select team', df['Team_name'].unique(), horizontal=True)

    # dropdown to select the player
    player = st.selectbox('Select player', df[df['Team_name'] == team]['Player_name'].unique())

    # dropdown to select the session
    session = st.selectbox('Select session', df[df['Player_name'] == player]['Session_Id'].unique())

    # filter the data based on the selected team
    filtered_df = df[(df['Player_name'] == player) & (df['Session_Id'] == session)]

    # chart for the GPS data
    gps_chart(filtered_df.copy())

    # show the filtered data
    st.header(f'GPS data for player *{player}* in session *{session}*')
    st.write(filtered_df)

    # the min and max values of the GPS data
    min_lat = df[['Lat_start', 'Lat_end']].min().min()
    max_lat = df[['Lat_start', 'Lat_end']].max().max()
    min_lon = df[['Lon_start', 'Lon_end']].min().min()
    max_lon = df[['Lon_start', 'Lon_end']].max().max()

    st.write('GPS data range of all records')
    st.write(f'Min Lat: {min_lat}, Max Lat: {max_lat}, Min Lon: {min_lon}, Max Lon: {max_lon}')

    # show the rows with the min and max values
    st.write('Rows with min and max values')
    st.write(df[(df['Lat_start'] == min_lat) | (df['Lat_end'] == min_lat) | (df['Lon_start'] == min_lon) | (df['Lon_end'] == min_lon)])
    st.write(df[(df['Lat_start'] == max_lat) | (df['Lat_end'] == max_lat) | (df['Lon_start'] == max_lon) | (df['Lon_end'] == max_lon)])

def gps_chart(df):
    st.header('Sprints in the session')

    pydeck_chart(df)

    altair_chart(df)

def altair_chart(df):
    # plot lines with starting Lat and Long and ending Lat and Long
    # range of Lat and Long should be the range of the football pitch
    range_lon = (10.45, 10.454)
    range_lat = (63.444, 63.446)

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Lon_start', scale=alt.Scale(domain=range_lon)),
        y=alt.Y('Lat_start', scale=alt.Scale(domain=range_lat)),
        x2='Lon_end',
        y2='Lat_end',
        color='Average_speed'
    )

    st.altair_chart(chart, use_container_width=True)

    # image of football pitch
    image_path = 'assets/pitch.png'
    # altair can only show images in base64 format
    image_base64 = gps.image_to_base64(image_path, image_format='PNG')
    source = pd.DataFrame({'url': [image_base64]})

    # show the image in the chart
    # rotate the image by 90 degrees
    chart = alt.Chart(source).mark_image(
    ).encode(
        url='url',
    ).properties(
        height=500,
    )

    st.altair_chart(chart, use_container_width=True)

def pydeck_chart(df):
    # coordinates of the football pitches
    pitch_coordinates = {
        'lat': [63.444589, 63.445152, 63.445640, 63.445077],
        'lon': [10.452373, 10.450687, 10.451500, 10.453186]
    }

    # convert the coordinates to list of lists for pydeck, with each list containing lon and lat
    pitch_points = [[lon, lat] for lat, lon in zip(pitch_coordinates['lat'], pitch_coordinates['lon'])]

    # use compute_view to set the zoom level
    view_state = pdk.data_utils.compute_view(pitch_points)
    # st.write('The view state is', view_state)

    # path for each sprint
    df['path'] = df.apply(lambda row: [[row['Lon_start'], row['Lat_start']], [row['Lon_end'], row['Lat_end']]], axis=1)
    # timestamps for each sprint. should be 32-bit floating numbers
    # todo: for now, set to 0 and 100; will be updated to actual timestamps later
    df['timestamps'] = df.apply(lambda row: [0, 100], axis=1)

    trips_layer = pdk.Layer(
        'TripsLayer',
        data=df,
        get_path='path',
        get_timestamps='timestamps',
        get_color=[253, 128, 93],
        opacity=0.8,
        width_min_pixels=2,
        current_time=100,
        trail_length=150,
    )

    st.write('Fading trails indicate the direction')

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-v9',
        initial_view_state=view_state,
        layers=[trips_layer],
    ))
