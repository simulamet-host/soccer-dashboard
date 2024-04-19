import altair as alt
import pydeck as pdk
import streamlit as st

from utils import data_fetcher

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
    gps_chart(filtered_df)

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
    st.subheader('Plot with notations')

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

def pydeck_chart(df):
    # plot on football pitch
    st.subheader('Plot on football pitch')

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

    # a line for each sprint
    line_layer = pdk.Layer(
        'LineLayer',
        data=df,
        get_source_position=['Lon_start', 'Lat_start'],
        get_target_position=['Lon_end', 'Lat_end'],
        # RGBA colors (red, green, blue, alpha); each value should be between 0 and 255
        get_color=[255, 0, 0, 180],
        get_width=2,
    )

    # circle for the end of each sprint
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position=['Lon_end', 'Lat_end'],
        get_fill_color=[255, 0, 0],
        get_radius=1,
    )
    st.write('The points are the end of each sprint')

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-v9',
        initial_view_state=view_state,
        layers=[line_layer, scatter_layer],
    ))
