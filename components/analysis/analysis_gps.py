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
    st.header('Sprints in the session')

    pydeck_chart(df)

    altair_chart(df)

def altair_chart(df):
    # show sprints on a uniform football pitch
    st.header('Sprints on a uniform football pitch')

    # get the local coordinates for the start and end points
    df['Lon_start_local'], df['Lat_start_local'], df['Lon_end_local'], df['Lat_end_local'], df ['Pitch_width'], df['Pitch_length'], _ = zip(*df.apply(lambda row: gps.local_coordinates_from_lat_lon(row['Lat_start'], row['Lon_start'], row['Lat_end'], row['Lon_end']), axis=1))

    # use pitch width and length as the scale domain for the y and x axes
    pitch_length = df['Pitch_length'].max()
    pitch_width = df['Pitch_width'].max()
    scaling_factor = 5

    # image of football pitch
    image_path = 'assets/pitch.png'
    # altair can only show images in base64 format
    image_base64 = gps.image_to_base64(image_path, image_format='PNG')
    source = pd.DataFrame({
        # 'x': length,
        # 'y': width,
        'url': [image_base64]
        })

    # show the image in the chart
    x_proportion, y_proportion, x_offset_p, y_offset_p = gps.image_proportion()
    pitch = alt.Chart(source).mark_image(
        # align='right',
        # baseline='top',
        height=50,
        width=50
    ).encode(
        x=alt.value(0),
        y=alt.value(0),
        url='url',
        # don't show tooltips about the image
        tooltip=alt.value(None)
    ).properties(
        # set matching width and height as scale domain so that the aspect ratio is correct
        # width=pitch_length * scaling_factor * x_proportion,
        # height=pitch_width * scaling_factor * y_proportion
    )

    # line connecting the start and end points
    lines = alt.Chart(df).mark_line(
    ).encode(
        x=alt.X('Lon_start_local', scale=alt.Scale(domain=(0, pitch_length))),
        y=alt.Y('Lat_start_local', scale=alt.Scale(domain=(0, pitch_width))),
        x2='Lon_end_local',
        y2='Lat_end_local',
    )

    st.altair_chart(pitch)
    # st.altair_chart(pitch + lines)

    # example test
    source = pd.DataFrame.from_records(
        [
            # {
            #     "x": 2.5,
            #     "y": 0.5,
            #     "img": "https://vega.github.io/vega-datasets/data/ffox.png",
            # },
            {
                "x": -60/4,
                "y": -29/4,
                "img": image_base64,
            },
            # {
            #     "x": 2.5,
            #     "y": 2.5,
            #     "img": "https://vega.github.io/vega-datasets/data/7zip.png",
            # },
        ]
    )

    pitch = alt.Chart(source).mark_image(
        width=1920/4,
        height=1218/4,
        aspect=False,
        align="left",
        baseline="bottom",
    ).encode(
        x=alt.X("x", scale=alt.Scale(domain=(-60/4, 1860/4)), axis=None),
        y=alt.Y("y", scale=alt.Scale(domain=(-29/4, 1189/4)), axis=None),
        url="img",
    ).properties(
        width=1920/4,
        height=1218/4
    )

    st.altair_chart(pitch)


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
