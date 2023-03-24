import pandas as pd
import matplotlib.pyplot as plt
#import mysql.connector

import streamlit as st
import pyarrow as pa

import missingno as msno
import plotly.express as px
import datetime
import numpy as np
import glob
import datetime

# Initialize MySQL connection.
# Uses st.cache_resource to only run once.
#@st.cache_resource
#def init_connection():
    #return mysql.connector.connect(**st.secrets["mysql"])

#conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min. > 6sec
#@st.cache_data(ttl=600)
#def run_query(query):
    #with conn.cursor() as cur:
        #cur.execute(query)
        #return cur.fetchall()

# Page configuration      
def gps_statistics():
   
   st.title("GPS Information")
   
   tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["Raw data ", "Map visualization", "Analysis", 
                                                "3d Map visualization", "2d Map visualization",
                                                "Players reports"])  
   
   #teams = pd.read_sql("SELECT * FROM gps",conn)
   #team_A = pd.read_sql("SELECT * FROM gps WHERE player_name LIKE 'TeamA%' ",conn)
   #team_B = pd.read_sql("SELECT * FROM gps WHERE player_name LIKE 'TeamB%' ",conn)
   #names = pd.read_sql("SELECT DISTINCT player_name FROM gps",conn)

   # Write a temporary Dataframe with gps coordinates
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
      # Define the options for the first selectbox
      Teams = ["Select a team",'Team_A', 'Team_B']
      selected_teams = st.selectbox("Team", Teams, key="Teams")

      # Define "Teams" for the second selectbox, based on the value of the first selectbox
      if selected_teams == "Team_A":
          Teams = [df_team_A]
      elif selected_teams == "Team_B":
          Teams = [df_team_B]

      # Define the options for the first selectbox
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
      
      if selected_teams == "Team_A":
         Players = team_A_player()
      elif selected_teams == "Team_B":
         Players = team_B_player()

      # Define date
      #df = pd.to_datetime(dataset['date'])
      st.date_input("Select a date (2019.06.01 or 2020.06.02)",datetime.date(2019, 6, 1))


   with tab1: # --- RAW DATA ---

      # Metric - no Dataframe accepted
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

      st.dataframe(dataset.sample(10))#.iloc[0:slider_number1])
      
      null = dataset.isnull().sum()  
      zero =dataset[dataset == 0].count()
      result = pd.concat([null, zero], axis=1,keys=["Count of missing values (null)", "Count of zero values (0)"])
      st.table (result)


   with tab2: # --- MAP VISUALIZATION ---
      
      st.subheader("Dataset selection")
      gps = pd.DataFrame(dataset[['lat', 'lon']])
      st.map(gps, zoom=11)

   with tab3: # --- ANALYSIS ---
      
# Sample size picking analyze 
      slider_analyse_1 = st.slider('1- Select the number of random rows to visualize', min_value=5, max_value=50, value=5, step=10)
      
# Radio button selection
      genre = st.radio("2- Select your favorite visualization",('Line plot','Bar plot','Scatter plot'))

# Plot color selection
      color = st.color_picker('3- Pick a color for your plot by clicking on the box', '#0034F9')
      
# Plot_1_TeamA_2020
      #if box == "TeamA_2020_2d44f941" :
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

# Plot_2_TeamA_2020
      #if box == "TeamA_2020_2d44f941" :
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

# Plot_3_TeamA_2020
      #if box == "TeamA_2020_2d44f941" :
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


   with tab4: #--- 3D_GPS_MAP ---

      #3d plot

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

   with tab5: #--- 2D_GPS_MAP ---

      #2d plot with slider
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
      image_filename = "Football.png" #'D:/Simula/Git 2023/soccer-dashboard/data/gps/Football.png'
      plotly_logo = base64.b64encode(open(image_filename, 'rb').read())

      #Add picture in background
      fig.update_layout(images= [dict(source='data:image/png;base64,{}'.format(plotly_logo.decode()),xref="paper", yref="paper"
         ,x=0, y=1,sizex=1, sizey=1,layer="below",opacity=0.75,)])
                    #xanchor="left",
                    #yanchor="top",
                    #sizing="stretch",
      st.plotly_chart(fig)
   
   with tab6: #--- Players reports ---

      st.write("")

      multi = st.multiselect('Choose your columns for your report',
                             ['Name','Team','Day','Training Duration (min)','Distance Traveled (m)','Average Speed (m/sec)', 'Number of stop'],
                             ['Name','Team'])
      st.write("")

      #Editable dataframe
      st.markdown ('Editable dataset : Modify or add cells by clicking on it')
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
      
       # Select only the columns selected with multiselect
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
          mime='text/csv',
)