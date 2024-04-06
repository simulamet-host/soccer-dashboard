import altair as alt
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

    st.write('GPS data range')
    st.write(f'Min Lat: {min_lat}, Max Lat: {max_lat}, Min Lon: {min_lon}, Max Lon: {max_lon}')

    # show the rows with the min and max values
    st.write('Rows with min and max values')
    st.write(df[(df['Lat_start'] == min_lat) | (df['Lat_end'] == min_lat) | (df['Lon_start'] == min_lon) | (df['Lon_end'] == min_lon)])
    st.write(df[(df['Lat_start'] == max_lat) | (df['Lat_end'] == max_lat) | (df['Lon_start'] == max_lon) | (df['Lon_end'] == max_lon)])

def gps_chart(df):
    st.header('Sprints in the session')

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
