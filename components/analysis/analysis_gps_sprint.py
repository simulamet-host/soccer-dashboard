import matplotlib.pyplot as plt
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

    st.header('Overview of GPS data')
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

    # highest and lowest average speed
    st.write('Highest and lowest average speed')
    st.write(df[df['Average_speed'] == df['Average_speed'].max()])
    st.write(df[df['Average_speed'] == df['Average_speed'].min()])
    # highest and lowest top speed
    st.write('Highest and lowest top speed')
    st.write(df[df['Top_speed'] == df['Top_speed'].max()])
    st.write(df[df['Top_speed'] == df['Top_speed'].min()])

    check_range(df)

def gps_chart(df):

    with st.expander('Sprints on map'):
        st.header('Sprints in the session')
        pydeck_chart(df)

    plt_chart(df)

def pydeck_chart(df):
    # path for each sprint
    df['path'] = df.apply(lambda row: [[row['Lon_start'], row['Lat_start']], [row['Lon_end'], row['Lat_end']]], axis=1)
    # timestamps for each sprint. should be 32-bit floating numbers
    # set to 0 and 100 because we only care about the start and end of the sprint
    df['timestamps'] = df.apply(lambda row: [0, 100], axis=1)

    # color the paths based on the average speed
    df['color'] = df['Average_speed'].apply(gps.get_color_from_speed)

    trips_layer = pdk.Layer(
        'TripsLayer',
        data=df,
        get_path='path',
        get_timestamps='timestamps',
        get_color='color',
        width_min_pixels=5,
        current_time=100,
        trail_length=200,
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 0],
    )

    # use the center of the Lat and Lon values as the initial view state
    mean_lat = df[['Lat_start', 'Lat_end']].mean().mean()
    mean_lon = df[['Lon_start', 'Lon_end']].mean().mean()
    view_state = pdk.ViewState(
        latitude=mean_lat,
        longitude=mean_lon,
        zoom=17,
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-v9',
        initial_view_state=view_state,
        layers=[trips_layer],
        tooltip={
            'html': 'Start: {Lat_start}, {Lon_start} <br> End: {Lat_end}, {Lon_end} <br> Average speed: {Average_speed} <br> Top speed: {Top_speed}',
            'style': {
                'color': 'white'
            }
        }
    ))

    st.write(f'Center of the map: Lat: {mean_lat}, Lon: {mean_lon}')
    st.write('Fading trails indicate the direction.')

    # because pydeck does not support color legend, we have to show the legend manually
    st.write('Average speed color legend:')
    html = gps.get_color_legend()
    st.write(html, unsafe_allow_html=True)

def plt_chart(df):
    # show sprints on a uniform football pitch
    st.header('Sprints on a uniform football pitch')

    fig, ax = plt.subplots()

    # local coordinates for the start and end points
    df['Lon_start_local'], df['Lat_start_local'], df['Lon_end_local'], df['Lat_end_local'], df ['Pitch_width'], df['Pitch_length'], _ = zip(*df.apply(lambda row: gps.local_coordinates_for_two_points(row['Lat_start'], row['Lon_start'], row['Lat_end'], row['Lon_end']), axis=1))

    # image of football pitch, with offset
    image_path = 'assets/pitch.png'
    image = plt.imread(image_path)
    extent = gps.pitch_image_extent(df['Pitch_length'].max(), df['Pitch_width'].max())
    extent = [-3.4870576440713417, 108.09878696621159, -1.6914846756940938, 69.35087170345784]
    ax.imshow(image, extent=extent)

    # color the sprints based on the average speed
    colors = df['Average_speed'].apply(gps.get_color_from_speed)
    # convert from [236, 218, 154] to hex RGB string, for matplotlib
    colors = colors.apply(lambda x: f'#{x[0]:02x}{x[1]:02x}{x[2]:02x}')

    # plot the sprints
    for index, row in df.iterrows():
        ax.plot([row['Lon_start_local'], row['Lon_end_local']], [row['Lat_start_local'], row['Lat_end_local']], linewidth=3, color=colors[index])

        # show an arrow at the end of the sprint
        ax.arrow(row['Lon_start_local'], row['Lat_start_local'], row['Lon_end_local'] - row['Lon_start_local'], row['Lat_end_local'] - row['Lat_start_local'], head_width=3, head_length=2, fc=colors[index], ec=colors[index])

    st.pyplot(fig)

    # show the color legend
    st.write('Average speed color legend:')
    html = gps.get_color_legend()
    st.write(html, unsafe_allow_html=True)

@st.cache_data()
def check_range(df):
    # show the rows with GPS data outside football pitches
    st.write('Rows with GPS data outside known football pitches')
    df['in_pitch'] = df.apply(lambda x: gps.in_pitch(x['Lat_start'], x['Lon_start']) and gps.in_pitch(x['Lat_end'], x['Lon_end']), axis=1)
    # add a link to google maps for the coordinates, in satellite view
    # insert the column after the Lon_end column
    df.insert(10, 'Google_maps_start', df.apply(lambda x: f'https://www.google.com/maps?t=k&q=loc:{x["Lat_start"]},{x["Lon_start"]}', axis=1))
    df.insert(11, 'Google_maps_end', df.apply(lambda x: f'https://www.google.com/maps?t=k&q=loc:{x["Lat_end"]},{x["Lon_end"]}', axis=1))
    st.dataframe(
        df[~df['in_pitch']],
        column_config={
            'Google_maps_start': st.column_config.LinkColumn(
                "Start", display_text="Map"
            ),
            'Google_maps_end': st.column_config.LinkColumn(
                "End", display_text="Map"
            )
        }
    )
