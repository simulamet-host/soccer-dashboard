import pandas as pd
import matplotlib.pyplot as plt
#import mysql.connector
import streamlit as st
#import pyarrow as pa
import plotly.express as px
import numpy as np
#import glob
import datetime
#import time
from haversine import haversine, Unit
import folium # pip install streamlit-folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

#start_time = time.time()
# # Connect to MySQL server
# # Uses st.cache_resource to only run once.
# @st.cache_resource#
# def connect():
#     cnx = mysql.connector.connect(**st.secrets["mysql"])
#     return cnx

# # Execute MySQL query
# # Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)#
# def execute_query(query, params=None):
#     cnx = connect()
#     cursor = cnx.cursor()
#     cursor.execute(query, params)
#     result = cursor.fetchall()
#     cursor.close()
#     cnx.close()
#     return result

# # MySQL connection message
# with st.spinner('Connecting to MySQL server...in a few seconds...'):
#     time.sleep(5)

# cnx = connect()
# if cnx.is_connected():
#     st.success('Connected to MySQL server!')

# else:
#     st.warning("Failed to connect to MySQL server.", icon="🚨") 

# Page configuration      
def gps_statistics():
   
   st.title("GPS Information")
   tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["Raw Data ", "Maps", "Session Analysis", "Performance Metrics","Player GPS Report", "Streamlit Pandas Profiling" ])
   
   # # Connection to DB
   # dataset = pd.read_sql("SELECT * FROM gps ORDER BY date, time ASC",cnx)
   # df_team_A = pd.read_sql("SELECT * FROM gps WHERE player_name LIKE 'TeamA%' ",cnx)
   # df_team_B = pd.read_sql("SELECT * FROM gps WHERE player_name LIKE 'TeamB%' ",cnx)
   # # names = pd.read_sql("SELECT DISTINCT player_name FROM gps",conn)

   # Write a temporary Dataframe with gps coordinates :
   
   # Random strings
   df_A = pd.DataFrame(np.random.randint(2019,2020,size=(25, 1)), columns=['date']).replace(to_replace=[2019,2020],value="20190601")
   df_B = pd.DataFrame(np.random.randint(2019,2020,size=(25, 1)), columns=['date']).replace(to_replace=[2019,2020],value="20200602")
   df = pd.concat([df_A,df_B],ignore_index=True)
   # Convert to date and keep only date without hours
   df = pd.to_datetime(df['date']).apply(lambda x: x.date())
   # Convert to date and keep only hours without date
   df0 = pd.DataFrame(np.random.randint(1200,1259,size=(50, 1)), columns=['time'])
   df0 = pd.to_datetime(df0['time'], format='%H%M').apply(lambda x: x.time())

   df_C = pd.DataFrame(np.random.randint(1,size=(25, 1)), columns=['player_name']).replace(to_replace=0,value="Player_1")
   df_D = pd.DataFrame(np.random.randint(1,size=(25, 1)), columns=['player_name']).replace(to_replace=0,value="Player_2") 
   df1 = pd.concat([df_C,df_D],ignore_index=True)
   
   df_E = pd.DataFrame(np.random.randint(1,size=(25, 1)), columns=['team']).replace(to_replace=0,value="Team_A")
   df_F = pd.DataFrame(np.random.randint(1,size=(25, 1)), columns=['team']).replace(to_replace=0,value="Team_B")
   df2 = pd.concat([df_E,df_F],ignore_index=True)

   df3 = pd.DataFrame(np.random.randint(0,100,size=(50, 5)), columns=['heart_rate','hacc', 'hdop','signal_quality','num_satellites', ])

   # Random floats
   df4 = pd.DataFrame(np.random.uniform(-0.005000,1.100000,size=(50, 8)), columns=['speed','inst_acc_impulse', 'accl_x','accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z'])
   df5 = pd.DataFrame(np.random.uniform(63.4440,63.4460,size=(50, 1)), columns=['lat'])
   df6 = pd.DataFrame(np.random.uniform(10.4510,10.4530,size=(50, 1)), columns=['lon'])
   # Concat
   team = pd.concat([df, df0, df1, df2, df3, df4, df5, df6], axis=1)
   
   # KPI
   # Calculate distance btw gps coordinates and create new column ['distance']
   team['distance'] = team.apply(lambda row: haversine((row['lat'], row['lon']), (row['lat'], row['lon']), unit=Unit.METERS), axis=1)
   dataset =team.sort_values(by='time')

   with st.sidebar:

      #team = st.selectbox("Select team", ['team_A', 'team_B'])

      df_team_A = dataset[(dataset['team'] == "Team_A")]  #dataset.drop_duplicates(subset = "team")
      df_team_B = dataset[(dataset['team'] == "Team_B")]    #dataset.drop_duplicates(subset = "team")
      df_player_A1 = df_team_A[(df_team_A["player_name"]== "Player_1")] 
      df_player_A2 = df_team_A[(df_team_A["player_name"]== "Player_2")]  #dataset.drop_duplicates(subset = "player_name") 
      df_player_B1 = df_team_B[(df_team_B["player_name"]== "Player_1")] 
      df_player_B2 = df_team_B[(df_team_B["player_name"]== "Player_2")] 
      #option_list_date = dataset['date'].unique()#.drop_duplicates(subset = "date")   
      
      st.write('')
      st.write('Full dataset by default if no selection:')
      
      ### BOX 1 (TEAM) ###

      # Define the options for the first selectbox
      Teams = ["Select a team",'Team_A', 'Team_B']
      selected_teams = st.selectbox("Team", Teams, key="Teams")

      # Define "Teams" for the second selectbox, based on the value of the first selectbox
      def A_teams ():
          if selected_teams == "Team_A":
              Teams = [df_team_A]
          elif selected_teams == "Team_B":
              Teams = [df_team_B]
      
      ### BOX 2 (PLAYERS) ###

      # Define the options for the first selectbox (Players)
      Players = ["Select a player",'Player_1', 'Player_2']
      selected_players = st.selectbox("Players", Players, key="Players")

      # Define "Players"
      def team_A_player ():
         if selected_players == "Player_1":
             Players = [df_player_A1]
         elif selected_players == "Player_2":
             Players = [df_player_A2]

      def team_B_player ():
         if selected_players == "Player_1":
             Players = [df_player_B1]
         elif selected_players == "Player_2":
             Players = [df_player_B2]
      
      ### BOX 3 (DATE) ### TO CONNECT

      # Define date
      st.date_input("Select a date (2019.06.01 or 2020.06.02)",datetime.date(2019, 6, 1))
      
      ### BOX 4 (SESSIONS) ### TO CONNECT

      # Define the options for the second selectbox (Session)
      # Sessions = ["Select a session",'Session_1', 'Session_2']
      # selected_sessions = st.selectbox("Sessions", Sessions, key="Session")

      # Define "Sessions" 
      # def A_Session ():
      #    if selected_sessions == "Session_1":
      #        Sessions = [df_Session_1]
      #    elif selected_sessions == "Session_2":
      #        Sessions = [df_Session_2]
      #    else : 
      #        Sessions = []

      # def B_Session ():
      #    if selected_sessions == "Session_1":
      #        Sessions = [df_Session_1]
      #    elif selected_sessions == "Session_2":
      #        Sessions = [df_Session_2]
      #    else : 
      #        Sessions = []


   with tab1: # --- RAW DATA --- TO REVIEW CONNECTION

      # Metrics
      st.write("")
      st.metric("Total number of rows in dataset", len(dataset)) # Metric

      # Dataset statistics board 
      st.header("Dataset statistics")
  
      if selected_teams == "Select a team":
         dataset = dataset
      if selected_teams == 'Team_A':
         dataset = df_team_A
      elif selected_teams == 'Team_B':
         dataset = df_team_B

      dataset_stat_board = st.dataframe(dataset.describe())

      # Dataset sample
      st.header("Dataset sample")
      st.write ("Select a cell and use command (Ctrl + F) to look for a specific value in the dataset")
      # Create checkbox
      highlight_max = st.checkbox('Highlight min and max values')

      # Display dataframe with max values highlighted when checkbox is selected
      if highlight_max:
          st.dataframe(dataset.sample(10).style.highlight_min(color = "red")\
                                               .highlight_max(color = "green"))
      else:
          st.dataframe(dataset.sample(10))
      
      # Missing data in Dataset
      st.header("Missing data in Dataset") 
      null = dataset.isnull().sum()  
      zero =dataset[dataset == 0].count()
      result = pd.concat([null, zero], axis=1,keys=["Count of missing values (null)", "Count of zero values (0)"])
     
      # Create checkbox
      highlight_max1 = st.checkbox('Highlight min and max values.')

      # Display dataframe with max values highlighted when checkbox is selected
      if highlight_max1:
          st.dataframe(result.style.highlight_min(color = "red")\
                                   .highlight_max(color = "green"), use_container_width=True)
      else:
          st.dataframe(result, use_container_width=True)


   with tab2: # --- MAP VISUALIZATION ---
      
      # # Map
      # st.subheader("Dataset selection")
      # gps = pd.DataFrame(dataset[['lat', 'lon']])
      # st.map(gps, zoom=11)

      # Static Map
      # Define the map's initial coordinates and zoom level
      map_center = (dataset['lat'].mean(), dataset['lon'].mean())

      # Create a base map
      m = folium.Map(location=map_center, zoom_start=17)

      # Function to add a marker to the map
      def add_marker(row):
          folium.Marker(location=(row['lat'], row['lon'])).add_to(m)

      # Connect the markers with a PolyLine
      coordinates = dataset[['lat', 'lon']].values.tolist()
      folium.PolyLine(locations=coordinates, color='blue', weight=1, opacity=1).add_to(m)

      # Display the map in Streamlit
      st.subheader("Dataset GPS Coordinates Map")
      st_folium(m, height=500, width=700, returned_objects=[])
      st.divider()

      # Animated Map
      # from folium.plugins import TimestampedGeoJson
      # # Define the map's initial coordinates and zoom level
      # map_center = (dataset['lat'].mean(), dataset['lon'].mean())

     # # Create a base map
      # m = folium.Map(location=map_center, zoom_start=17, control_scale=True)

      # # Create a GeoJSON object with the coordinates and timestamps
      # geo_json_data = {
      #     'type': 'FeatureCollection',
      #     'features': [
      #         {
      #             'type': 'Feature',
      #             'geometry': {
      #                 'type': 'Point',
      #                 'coordinates': [row['lon'], row['lat']]
      #             },
      #             'properties': {
      #                 'time': row['time'].strftime('%Y-%m-%dT%H:%M:%S'),  # Convert time to string format
      #                 'style': {'color': 'blue'}
      #             }
      #         }
      #         for _, row in dataset.iterrows()
      #     ]
      # }

      # # Add the TimestampedGeoJson plugin to the map
      # TimestampedGeoJson(
      #     geo_json_data,
      #     period='PT30S',  # Display one marker per 30 sec
      #     add_last_point=True,
      #     auto_play=True,
      #     loop=True,
      #     max_speed=1,
      #     loop_button=True,
      #     date_options='YYYY-MM-DDTHH:mm:ss',
      #     time_slider_drag_update=True
      # ).add_to(m)

      # # Connect the markers with a PolyLine
      # coordinates = dataset[['lat', 'lon']].values.tolist()
      # folium.PolyLine(locations=coordinates, color='blue', weight=1, opacity=1).add_to(m)

      # # Display the map in Streamlit
      # st.subheader("Dataset GPS Coordinates Map with Animation")
      # st_folium(m, height=500, width=700, returned_objects=[])


      # # Add MarkerCluster for better visualization of markers
      # marker_cluster = MarkerCluster().add_to(m)

      # # Add markers for each GPS coordinate
      # for lat, lon in zip(dataset['lat'], dataset['lon']):
      #      folium.Marker(location=[lat, lon]).add_to(marker_cluster)

      #2d plot with slider
      st.header("")
      st.subheader("2D Animation of selected player's movements on field")
      fig = px.scatter(dataset, x='lon', y='lat',color='player_name', animation_frame="time",animation_group="player_name", width=1009, height=750)#color_discrete_sequence=['red', 'cornflowerblue'],width=1009, height=811
      #Change duration of transition
      fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2500
      fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 2500
      #Resizing axes
      fig.update_layout(yaxis_range=[63.4440,63.4460])
      fig.update_layout(xaxis_range=[10.4510,10.4530])
      #Removing background lines
      fig.update_xaxes(showgrid=True, zeroline=True)
      fig.update_yaxes(showgrid=True, zeroline=True)
      #Marker update
      fig.update_traces(marker=dict(size=9,line=dict(width=2,color='black')),selector=dict(mode='markers'))
      #Set a local image as a background
      import base64
      image_filename = './src/assets/soccer-field.png'
      plotly_logo = base64.b64encode(open(image_filename, 'rb').read())

      #Add picture in background
      fig.update_layout(images= [dict(source='data:image/png;base64,{}'.format(plotly_logo.decode()),xref="paper", yref="paper"
         ,x=0, y=1,sizex=1, sizey=1,layer="below",opacity=0.75,)])
                    #xanchor="left",
                    #yanchor="top",
                    #sizing="stretch",
      st.plotly_chart(fig)

      #3d plot
      st.header("")
      st.subheader("3D plot of selected player's movements on field")
      fig = px.line_3d(dataset, x='lon', y='lat', z='time',color='player_name')#, animation_frame="time",animation_group="player_name")
      fig.update_layout(yaxis_range=[63.4440,63.4460])
      fig.update_layout(xaxis_range=[10.4510,10.4530])
      #Marker update
      fig.update_traces(marker=dict(size=6,line=dict(width=2,color='black')),selector=dict(mode='markers'))
      #Background color
      fig.update_layout(scene = dict(
                    zaxis = dict(
                         backgroundcolor="green",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",)),
                    width=900,
                    margin=dict(r=10, l=10,b=10, t=10))
      st.plotly_chart(fig)

   with tab3: # --- ANALYSIS ---
      
# Sample size picking analyze 
      slider_analyse_1 = st.slider('1- Select the number of random rows to visualize', min_value=5, max_value=50, value=5, step=10)
      
# Radio button selection
      genre = st.radio("2- Select your favorite visualization",('Line plot','Bar plot','Scatter plot'))

# Plot color selection
      color = st.color_picker('3- Pick a color for your plot by clicking on the box', '#0034F9')
      
# Plot_1
 
      st.header("Heart rate over Time")
      if genre == 'Bar plot':
         fig = px.bar((dataset.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
         plot= st.plotly_chart(fig, use_container_width=True) 
      elif genre == 'Line plot':
         fig = px.line((dataset.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
         plot = st.plotly_chart(fig, use_container_width=True)   
      elif genre == 'Scatter plot':
         fig = px.scatter((dataset.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
         plot = st.plotly_chart(fig, use_container_width=True)  

# Plot_2
 
      st.header("Acceleration over Time")
      if genre == 'Line plot':
         fig = px.line((dataset.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
         st.plotly_chart(fig, use_container_width=True) 
      elif genre == 'Bar plot':
         fig = px.bar((dataset.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
         st.plotly_chart(fig, use_container_width=True)   
      elif genre == 'Scatter plot':
         fig = px.scatter((dataset.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
         st.plotly_chart(fig, use_container_width=True) 

# Plot_3

      st.header("Rotation over Time")
      if genre == 'Line plot':
         fig = px.line((dataset.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
         st.plotly_chart(fig, use_container_width=True)    
      elif genre == 'Bar plot':
         fig = px.bar((dataset.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
         st.plotly_chart(fig, use_container_width=True)
      elif genre == 'Scatter plot':
         fig = px.scatter((dataset.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
         st.plotly_chart(fig, use_container_width=True) 

   
   with tab4: #--- Players reports ---

      st.write("")

      multi = st.multiselect('Choose your columns for your report',
                             ['Name','Team','Day','Training Duration (min)','Distance Traveled (m)','Average Speed (m/sec)', 'Number of stop'],
                             ['Name','Team'])
      st.write("")

      #Editable dataframe
      st.markdown ('Editable dataset : Modify or add cells by clicking on cells')
      data_report = {'Name': ['Player_1', 'Player_2'],
                     'Team': ['Team_A', 'Team_B'],
                     'Day': ["01.06.2019", '02.06.2020'],
                     'Training Duration (min)': [120, 160],
                     'Distance Traveled (m)': [2000, 3000],
                     'Average Speed (m/sec)': [2.4, 3.6], 
                     'Number of stop':[10,20]}
      #data_report = multi
      df_report = pd.DataFrame (data_report)
      st.experimental_data_editor (df_report,num_rows="dynamic")

      # Use loc function to select only the columns that were selected in the multiselect
      if multi:
        df_report = df_report.loc[:, multi]

      #Download button
      #Cache the conversion to prevent computation on every rerun
      @st.cache_resource
      def convert_df(df_report):
          return df_report.to_csv().encode('utf-8')

      csv = convert_df(df_report)
      
      st.write("")
      st.markdown ("Download report as '.csv' file:")
      st.write("")
      st.download_button(
          label="Click to download",
          data=csv,
          file_name='Players_report.csv',
          mime='text/csv',)

   
   with tab5: #--- Player GPS Report --- IT HAS TO BE AN INDEPENDANT PAGE FROM SIDEBAR : ANOTHER PY.FILE

      st.write("")
      st.write("Select players to be compared:")
      col1, col2 = st.columns(2)
      
      with col1:
         Team = ["Select a team",'Team_A', 'Team_B']
         selected_players = st.selectbox("Team", Team, key="Team0")

         Players = ["Select a player",'Player_1', 'Player_2']
         selected_players = st.selectbox("Player", Players, key="PlayerA")  
         
         st.date_input("Select a date",datetime.date(2022, 1, 1), key= "date1")  

         Session = ["Select a session",'Session_1', 'Session_2']
         selected_players = st.selectbox("Session",Session, key="Session")    
      
         st.write("")
         # multi2 = st.multiselect('Select KPI:',
         #                        ['Training Duration (min)','Distance Traveled (m)','Average Speed (m/sec)', 'Number of stop'],
         #                        ['Training Duration (min)'])

         multi1 = st.multiselect('Select a column:',['time','heart_rate','speed','inst_acc_impulse', 'distance'],['time', 'heart_rate'], key='A')
         #,'accl_x','accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z','hacc', 'hdop','signal_quality','num_satellites',
         
         # Use loc function to select only the columns that were selected in the multiselect
         df_1 = dataset
         if multi1:
            df_1 = df_1.loc[:, multi1]

         st.dataframe (df_1)
         st.subheader("")

         # Plot selected columns
         x = 'time'
         y = ', '.join(multi1)
         st.subheader(f" {y} over {x}")
         if not df_1.empty:
             fig = px.line(df_1, x='time', y=multi1)
             st.plotly_chart(fig, use_container_width=True)
         else:
             st.write("Please select at least one column to plot.") 

         # Plot KPI
         from plotly.subplots import make_subplots
         import plotly.graph_objects as go
         st.subheader("")
         st.subheader('Mixed Subplots')
         fig = make_subplots(rows=2, cols=2,specs=[[{"type": "xy"}, {"type": "polar"}],[{"type": "domain"}, {"type": "scene"}]],)
         fig.add_trace(go.Bar(y=[2, 3, 1]), row=1, col=1)
         fig.add_trace(go.Barpolar(theta=[0, 45, 90], r=[2, 3, 1]),  row=1, col=2)
         fig.add_trace(go.Pie(values=[2, 3, 1]), row=2, col=1)
         fig.add_trace(go.Scatter3d(x=[2, 3, 1], y=[0, 0, 0],z=[0.5, 1, 2], mode="lines"),row=2, col=2)
         fig.update_layout(height=700, showlegend=False)
         st.plotly_chart(fig, use_container_width=True) 

      with col2:
         
         Team = ["Select a team",'Team_A', 'Team_B']
         selected_players = st.selectbox("Team", Team, key="Team1")

         Players = ["Select a player",'Player_1', 'Player_2']
         selected_players = st.selectbox("Player", Players, key="PlayerB")  
         
         st.date_input("Select a date",datetime.date(2022, 1, 1), key= "date2")  

         Session = ["Select a Session",'Session_1', 'Session_2']
         selected_players = st.selectbox("Session",Session, key="Session1") 

         st.write("")
         # Select columns to display
         multi2 = st.multiselect('Select column:',['time','heart_rate','speed','inst_acc_impulse', 'distance'],['time', 'heart_rate'], key='B')
         #,'accl_x','accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z','hacc', 'hdop','signal_quality','num_satellites',
         
         # Use loc function to select only the columns that were selected in the multiselect
         df_2 = dataset
         if multi2:
            df_2 = df_2.loc[:, multi2]
         
         # Display selected columns in a dataframe
         st.dataframe (df_2)  
         st.subheader("")

         # Plot selected columns
         x = 'time'
         y = ', '.join(multi2)
         st.subheader(f"{y} over {x}") # Put the title in accordance to selection automatically
         if not df_2.empty:
             fig = px.line(df_2, x='time', y=multi2)
             st.plotly_chart(fig, use_container_width=True)
         else:
             st.write("Please select at least one column to plot.") 

         # Plot KPI
         from plotly.subplots import make_subplots
         import plotly.graph_objects as go
         st.subheader("")
         st.subheader('Mixed Subplots')
         fig = make_subplots(rows=2, cols=2,specs=[[{"type": "xy"}, {"type": "polar"}],[{"type": "domain"}, {"type": "scene"}]],)
         fig.add_trace(go.Bar(y=[2, 3, 1]), row=1, col=1)
         fig.add_trace(go.Barpolar(theta=[0, 45, 90], r=[2, 3, 1]),  row=1, col=2)
         fig.add_trace(go.Pie(values=[2, 3, 1]), row=2, col=1)
         fig.add_trace(go.Scatter3d(x=[2, 3, 1], y=[0, 0, 0],z=[0.5, 1, 2], mode="lines"),row=2, col=2)
         fig.update_layout(height=700, showlegend=False)
         st.plotly_chart(fig, use_container_width=True) 

      # Plot differences final
      st.subheader ("Comparing Subplots")
      fig = make_subplots(rows=2, cols=1)
      fig.append_trace(go.Scatter(x=[3, 4, 5],y=[1000, 1100, 1200],), row=1, col=1)
      fig.append_trace(go.Scatter(x=[2, 3, 4],y=[100, 110, 120],), row=2, col=1)
      fig.update_layout(height=600, width=600)
      st.plotly_chart(fig, use_container_width=True) 

      # # Plot differences
      # x = 'time'
      # y = ', '.join(multi2)
      # st.subheader(f"Comparaison of {y} over {x}")
      # fig = px.line(df_1, x=x, y=multi2*len(multi2))
      # st.plotly_chart(fig, use_container_width=True)  

# # Evaluate code time
# end_time = time.time()
# GPSpage = st.write("Time taken charging page:", end_time - start_time, "seconds")

   with tab6:

      import pandas_profiling
      from streamlit_pandas_profiling import st_profile_report

      df = dataset#pd.read_csv("https://storage.googleapis.com/tf-datasets/titanic/train.csv")
      pr = df.profile_report()

      st_profile_report(pr)