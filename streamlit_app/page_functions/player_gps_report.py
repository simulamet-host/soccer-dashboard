import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
import datetime
import numpy as np
import time
from haversine import haversine, Unit
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import page_functions.queries as qu
#start_time = time.time()

# Connect to MySQL server
# Uses st.cache_resource to only run once.
#@st.cache_resource# doesn't work

conn = qu.conn
# Execute MySQL query
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=60)# doesn't work
def execute_query(query, params=None):
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# MySQL connection message
with st.spinner('Connecting to MySQL server...in a few seconds...'):
    time.sleep(5)

if conn.is_connected():
    st.success('Connected to MySQL server!')

else:
    st.warning("Failed to connect to MySQL server.", icon="🚨") 

# Page configuration      
def player_gps_statistics():
   
   st.title("Player GPS Report")
   #tab1= st.tabs(["Player GPS Report" ])  
   
   # Connection to DB
   dataset = pd.read_sql(qu.dataset, conn)
   df_team_A = pd.read_sql(qu.df_team_A, conn)
   df_team_B = pd.read_sql(qu.df_team_B, conn)
   Players_list = dataset
   # names = pd.read_sql("SELECT DISTINCT player_name FROM gps",conn)

   # KPI
   # Calculate distance btw gps coordinates and create new column ['distance']
   # dataset['distance'] = dataset.apply(lambda row: haversine((row['lat'], row['lon']), (row['lat'], row['lon']), unit=Unit.METERS), axis=1)
   # Error: Unrecognized type: "Duration" (18)

   st.write("")
   st.write("Select players to be compared:")

   ### BOX 1 (TEAM) ###
   # Define "Teams" for the second selectbox, based on the value of the first selectbox
   def A_B_teams ():
      if selected_teams == "Team_A":
          Teams = df_team_A
      elif selected_teams == "Team_B":
          Teams = df_team_B   

   # Define the options for the first selectbox
   Teams = ["Select a team",'Team_A', 'Team_B']
   selected_teams = st.selectbox("Team", Teams, key="Teams1")

   def A_B_players ():
       if selected_teams == "Team_A":
           Players_list = df_team_A['player_name'].tolist()
       elif selected_teams == "Team_B":
           Players_list= df_team_B['player_name'].tolist() 
      
   # Define the options for the first selectbox (Players)
   Players = ["Select a player",Players_list]
   selected_players = st.selectbox("Players", Players, key="Players1")


   col1, col2 = st.columns(2)

   with col1:

      ### BOX 2 (PLAYERS) ###
      # Define "Players"
      # def A_player ():
      #    if selected_players == "Player_1":
      #        Players = df_player_A1
      #    elif selected_players == "Player_2":
      #        Players = df_player_A2

      # def B_player ():
      #    if selected_players == "Player_1":
      #        Players = df_player_B1
      #    elif selected_players == "Player_2":
      #        Players = df_player_B2



      ### BOX 3 (DATE) ### TO CONNECT

      # Date filter
      selected_date =st.date_input("Select a date (2019.06.01 or 2020.06.02)",datetime.date(2019, 6, 1),key="Date1")

      # Filter dataset based on selected player and date
      # if selected_players == "Player_1":
      #     df_player = df_player_A1
      # elif selected_players == "Player_2":
      #     df_player = df_player_A2

      # # Filter data based on selected player and date
      # filtered_data = your_data_frame[(your_data_frame['Player'].isin(Players)) & (your_data_frame['Date'] == selected_date)]
      # st.write(filtered_data)

      ### BOX 4 (SESSIONS) ### TO CONNECT

      # Define the options for the second selectbox (Session)
      Sessions = ["Select a session",'Session_1', 'Session_2']
      selected_sessions = st.selectbox("Sessions", Sessions, key="Session1")

      # Define "Sessions" 
      def A_Session ():
         if selected_sessions == "Session_1":
             Sessions = [df_Session_1]
         elif selected_sessions == "Session_2":
             Sessions = [df_Session_2]
         else : 
             Sessions = []

      def B_Session ():
         if selected_sessions == "Session_1":
             Sessions = [df_Session_1]
         elif selected_sessions == "Session_2":
             Sessions = [df_Session_2]
         else : 
             Sessions = []
      
      # if selected_teams == "Team_A":
      #    Players = team_A_player()
      # elif selected_teams == "Team_B":
      #    Players = team_B_player()   
   
      st.write("")
      # Multiselect 'Column'
      multi1 = st.multiselect('Select KPI:',['time','heart_rate','speed','inst_acc_impulse', 'distance'],['time', 'heart_rate'], key='A')
      #,'accl_x','accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z','hacc', 'hdop','signal_quality','num_satellites',
      
      # Use loc function to select only the columns that were selected in the multiselect
      df_1 = dataset
      if multi1:
         df_1 = df_1.loc[:, multi1]

      st.dataframe (df_1)
      st.divider()

      # Plot selected columns
      x = 'time'
      y = ', '.join(multi1)
      st.subheader(f" {y} over {x}")
      if not df_1.empty:
          fig = px.line(df_1, x='time', y=multi1)
          st.plotly_chart(fig, use_container_width=True)
      else:
          st.write("Please select at least one KPI to plot.") 

      # Plot KPI
      import plotly.graph_objects as go
      st.divider()
      st.subheader('Mixed Subplots')
      fig = make_subplots(rows=2, cols=2,subplot_titles=("Bars", "Covered Area", "Pie", "3d accl"),
                          specs=[[{"type": "xy"}, {"type": "polar"}],[{"type": "domain"}, {"type": "scene"}]],)
      fig.add_trace(go.Bar(name='time', x=[2, 3, 1], y=[20, 14, 23]))
      fig.add_trace(go.Barpolar(theta=[0, 45, 90], r=[2, 3, 1]),  row=1, col=2)
      fig.add_trace(go.Pie(values=[2, 3, 1]), row=2, col=1)
      fig.add_trace(go.Scatter3d(x=dataset['accl_x'], y=dataset['accl_y'],z=dataset['accl_z'], mode="lines"),row=2, col=2)
      fig.update_layout(height=700, showlegend=False)
      st.plotly_chart(fig, use_container_width=True) 
      #The 'type' property specifies the trace type One of: 
      #['bar', 'barpolar', 'box', 'candlestick', 'carpet', 'choropleth', 'choroplethmapbox', 'cone', 'contour', 'contourcarpet', 'densitymapbox', 
      #'funnel', 'funnelarea', 'heatmap', 'heatmapgl', 'histogram', 'histogram2d', 'histogram2dcontour', 'icicle', 'image', 'indicator', 'isosurface',
      #'mesh3d', 'ohlc', 'parcats', 'parcoords', 'pie', 'pointcloud', 'sankey', 'scatter', 'scatter3d', 'scattercarpet', 'scattergeo', 'scattergl', 
      #'scattermapbox', 'scatterpolar', 'scatterpolargl', 'scattersmith', 'scatterternary', 'splom', 'streamtube', 'sunburst', 'surface', 'table',
      # 'treemap', 'violin', 'volume', 'waterfall'] 
      #- All remaining properties are passed to the constructor of the specified trace type (e.g. [{'type': 'scatter', ...}, {'type': 'bar, ...}])
      st.divider()

   with col2:     

      ### BOX 3 (DATE) ###

      # Date filter
      selected_date =st.date_input("Select a date (2019.06.01 or 2020.06.02)",datetime.date(2019, 6, 1),key="Date2")

      # Filter dataset based on selected player and date
      # if selected_players == "Player_1":
      #     df_player = df_player_A1
      # elif selected_players == "Player_2":
      #     df_player = df_player_A2

      # # Filter data based on selected player and date
      # filtered_data = your_data_frame[(your_data_frame['Player'].isin(Players)) & (your_data_frame['Date'] == selected_date)]
      # st.write(filtered_data)
      
      ### BOX 4 (SESSIONS) ###

      # Define the options for the second selectbox (Session)
      Sessions = ["Select a session",'Session_1', 'Session_2']
      selected_sessions = st.selectbox("Sessions", Sessions, key="Session2")

      # # Define "Sessions"
      def A_Session ():
         if selected_sessions == "Session_1":
             Sessions = [df_Session_1]
         elif selected_sessions == "Session_2":
             Sessions = [df_Session_2]

      def B_Session ():
         if selected_sessions == "Session_1":
             Sessions = [df_Session_1]
         elif selected_sessions == "Session_2":
             Sessions = [df_Session_2]
    
      st.write("")
      # Select columns to display
      multi2 = st.multiselect('Select KPI:',['time','heart_rate','speed','inst_acc_impulse', 'distance'],['time', 'heart_rate'], key='B')
      #,'accl_x','accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z','hacc', 'hdop','signal_quality','num_satellites',
      
      # Use loc function to select only the columns that were selected in the multiselect
      df_2 = dataset
      if multi2:
         df_2 = df_2.loc[:, multi2]
      
      # Display selected columns in a dataframe
      st.dataframe (df_2)  
      st.divider()

      # Plot selected columns
      x = 'time'
      y = ', '.join(multi2)
      st.subheader(f"{y} over {x}") # Put the title in accordance to selection automatically
      if not df_2.empty:
          fig = px.line(df_2, x='time', y=multi2)
          st.plotly_chart(fig, use_container_width=True)
      else:
          st.write("Please select at least one KPI to plot.") 

      # Plot KPI

      st.divider()
      st.subheader('Mixed Subplots')
      fig = make_subplots(rows=2, cols=2,subplot_titles=("Bars", "Covered Area", "Pie", "3d gyro"),
                          specs=[[{"type": "xy"}, {"type": "polar"}],[{"type": "domain"}, {"type": "scene"}]],)
      fig.add_trace(go.Bar(y=[2, 3, 1]), row=1, col=1)
      fig.add_trace(go.Barpolar(theta=[0, 45, 90], r=[2, 3, 1]),  row=1, col=2)
      fig.add_trace(go.Pie(values=[2, 3, 1]), row=2, col=1)
      fig.add_trace(go.Scatter3d(x=dataset['gyro_x'], y=dataset['gyro_y'],z=dataset['gyro_z'], mode="lines"),row=2, col=2)
      fig.update_layout(height=700, showlegend=False)
      st.plotly_chart(fig, use_container_width=True)
      st.divider() 

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
