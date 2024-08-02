import matplotlib.pyplot as plt
import streamlit as st

from utils import data_fetcher
from utils import gps

def view():
    # fetch the data from the database
    table = 'LH_HIR'
    columns = ['*']
    df = data_fetcher.fetch_data(table, columns)

    # select data
    with st.expander('**Select data**', expanded=True):
        # radio button to select the team
        team = st.radio('Select team', df['Team_name'].unique(), horizontal=True)

        # dropdown to select the player
        player = st.selectbox('Select player', df[df['Team_name'] == team]['Player_name'].unique())

        # dropdown to select the session
        session = st.selectbox('Select session', df[df['Player_name'] == player]['Session_Id'].unique())

    # select style
    with st.expander('**Customize style**', expanded=True):
        # use satellite view or pitch view
        view = st.radio('Select view', ['Satellite view', 'Pitch view', 'Both'], horizontal=True)

        # display arrowhead at the end of the sprint
        arrowhead = st.radio('Display arrowhead at the end of the sprint', ['Yes', 'No'], horizontal=True)

        # pick color scheme
        col1, col2 = st.columns([1, 3], vertical_alignment='bottom')
        # the options
        with col1:
            color_scheme = st.radio('Pick color scheme', ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu'], index=7)
        # the image showing the color scheme
        with col2:
            st.image('assets/colormaps.png', width=300)

    # filter the data based on the selected team
    filtered_df = df[(df['Player_name'] == player) & (df['Session_Id'] == session)]

    # color the sprints based on the average speed
    # normalize the speed from the whole dataset, so the color is consistent
    norm = plt.Normalize(df['Average_speed'].min(), df['Average_speed'].max())

    # chart for the GPS data
    gps_chart(filtered_df.copy(), norm, view, arrowhead, color_scheme)

    show_data(filtered_df, player, session, df)

def show_data(filtered_df, player, session, df):
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

    # check_range(df)

def gps_chart(df, norm, view, arrowhead, color_scheme):
    if view == 'Satellite view' or view == 'Both':
        satel_chart(df, norm, arrowhead, color_scheme)
    if view == 'Pitch view' or view == 'Both':
        pitch_chart(df, norm, arrowhead, color_scheme)

    # the positioning of the pitch view and the satellite view is not matching perfectly
    # tried using matplotlib.transforms.Affine2D().rotate_deg_around() to rotate the plot, but the result is also not perfect

def satel_chart(df, norm, arrowhead, color_scheme):
    st.header('Satellite view')
    fig, ax = plt.subplots(figsize=(4.5, 4.5))

    # use the mean of the Lat and Lon values to find the pitch
    mean_lat = df[['Lat_start', 'Lat_end']].mean().mean()
    mean_lon = df[['Lon_start', 'Lon_end']].mean().mean()
    pitch = gps.find_pitch(mean_lat, mean_lon)
    if pitch is None:
        st.write('Cannot find pitch information')
        return

    # use the center of the pitch to determine the satellite image
    center_lat, center_lon = pitch['center']
    image, extent = gps.fetch_sat_img(center_lat, center_lon)

    # ax.set_xlim(extent[0], extent[1])
    # ax.set_ylim(extent[2], extent[3])
    # setting 'extent' changes the aspect ratio, so we need to set the ratio to keep the original aspect ratio of the image
    aspect = (image.height / image.width) * (extent[1] - extent[0]) / (extent[3] - extent[2])
    ax.imshow(image, extent=extent, aspect=aspect)

    # set the colormap
    cmap = plt.cm.get_cmap(color_scheme)

    # plot the sprints
    for index, row in df.iterrows():
        color = cmap(norm(row['Average_speed']))
        ax.plot([row['Lon_start'], row['Lon_end']], [row['Lat_start'], row['Lat_end']], linewidth=1, color=color)

        if arrowhead == 'Yes':
            # show an arrowhead at the end of the sprint
            ax.arrow(row['Lon_start'], row['Lat_start'], row['Lon_end'] - row['Lon_start'], row['Lat_end'] - row['Lat_start'], width=0.000001, fc=color, ec=color, head_width=0.00003)

    # colorbar for the average speed
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, ax=ax, label='Average speed (m/s)', shrink=0.7)

    # hide the axis
    ax.axis('off')

    # attribution for the map (Mapbox, etc.)
    attr_map(ax)

    st.pyplot(fig, use_container_width=False)

def attr_map(ax):
    # show Mapbox logo at the bottom left corner
    mapbox_logo = plt.imread('assets/mapbox-logo-white.png')
    inset_ax = ax.inset_axes([0.01, -0.04, 0.14, 0.14])
    inset_ax.imshow(mapbox_logo)
    inset_ax.axis('off')
    # add text attribution at the bottom right corner
    text_attribution = '© Mapbox © OpenStreetMap Improve this map © Maxar'
    ax.text(0.99, 0.01, text_attribution, color='white', ha='right', va='bottom', transform=ax.transAxes, fontsize=4.8)

def pitch_chart(df, norm, arrowhead, color_scheme):
    # show sprints on a uniform football pitch
    st.header('Pitch view')

    fig, ax = plt.subplots(figsize=(4.5, 4.5))

    method = 'utm'
    result_start = gps.convert_coordinates(df['Lat_start'], df['Lon_start'], method=method)
    result_end = gps.convert_coordinates(df['Lat_end'], df['Lon_end'], method=method)
    if result_start is None or result_end is None:
        st.write('Pitch not found')
        return
    coords_start, pitch = result_start
    coords_end, _ = result_end
    df['ux_start'], df['uy_start'] = coords_start
    df['ux_end'], df['uy_end'] = coords_end

    # image of football pitch, with offset
    image_path = 'assets/pitch.png'
    image = plt.imread(image_path)
    extent = gps.pitch_image_extent(pitch['length'], pitch['width'])
    ax.imshow(image, extent=extent)

    # set the colormap
    cmap = plt.cm.get_cmap(color_scheme)

    # plot the sprints
    for index, row in df.iterrows():
        color = cmap(norm(row['Average_speed']))
        ax.plot([row['ux_start'], row['ux_end']], [row['uy_start'], row['uy_end']], linewidth=2, color=color)

        if arrowhead == 'Yes':
            # show an arrowhead at the end of the sprint
            ax.arrow(row['ux_start'], row['uy_start'], row['ux_end'] - row['ux_start'], row['uy_end'] - row['uy_start'], head_width=2, head_length=1.5, fc=color, ec=color)

    # colorbar for the average speed
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, ax=ax, label='Average speed (m/s)', shrink=0.6, orientation='horizontal')

    st.pyplot(fig, use_container_width=False)

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
