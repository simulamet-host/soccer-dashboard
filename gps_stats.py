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
   
   tab1, tab2, tab3, tab4, tab5= st.tabs(["Raw data ", "Map visualization", "Analysis", "3d Map visualization", "2d Map visualization"])  
   
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
   df = pd.to_datetime(df['date'])#.apply(lambda x: x.date())
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
   team1 =team.sort_values(by='time')

   with st.sidebar:
      st.write('')

      #team = st.selectbox("Select team", ['team_A', 'team_B'])

      list_team_A = team1[(team1['team'] == "Team_A")]  #team1.drop_duplicates(subset = "team")
      list_team_B = team1[(team1['team'] == "Team_B")]    #team1.drop_duplicates(subset = "team")
      list_player_1 = team1[(team1["player_name"]== "Player_1")] 
      list_player_2 = team1[(team1["player_name"]== "Player_2")]  #team1.drop_duplicates(subset = "player_name")  
      #option_list_date = team1['date'].unique()#.drop_duplicates(subset = "date")   


      # Define the options for the first selectbox
      Teams = ['Team_A', 'Team_B']
      selected_teams = st.selectbox("Select a team", Teams, key="Teams")

      # Define "Teams" for the second selectbox, based on the value of the first selectbox
      if selected_teams == "Team_A":
          Teams = [list_team_A]
      elif selected_teams == "Team_B":
          Teams = [list_team_B]

      # Define the options for the first selectbox
      Players = ['Players_1', 'Players_2']
      selected_players = st.selectbox("Select a player", Players, key="Players")
      # Define "Players"
      if selected_players == "Players_1":
          Players = [list_player_1]
      elif selected_players == "Players_2":
          Players = [list_player_2]

      # Define date
      #df = pd.to_datetime(team1['date'])
      st.date_input("Select a date (01.06.2019 or 02.06.2020)",datetime.date(2019, 6, 1))

   with tab1: # --- RAW DATA ---

      # Metric - no Dataframe accepted
      st.write("")
      st.metric("Total number of rows in dataset", len(team1)),#('TeamA-2d44f941')) # Metric

 
      #d1 = team11.drop(columns=['id','time'])   
      #st.dataframe (d1)
      #d2 = team12.drop(columns=['id','time'])
      #st.dataframe (d2)

      # Dataset statistics board 
      st.header("Dataset statistics")
      #teams1 = teams.drop(columns=['id','time'])
      st.dataframe(team1.describe())

      # Dataset sample
      st.header("Dataset sample")
      st.dataframe(team1.sample(10))#.iloc[0:slider_number1])

      # Plot sample board "Missing data"
      #st.header("Missing data in dataset")
      #miss = msno.matrix(team1)#,figsize=(5,3))
      #st.pyplot(miss.figure)
      #st.write("#")
      
      null = team1.isnull().sum()  
      zero =team1[team1 == 0].count()
      result = pd.concat([null, zero], axis=1,keys=["Count of missing values (null)", "Count of zero values (0)"])
      st.table (result)


   with tab2: # --- MAP VISUALIZATION ---
      
      st.subheader("Dataset selection")
      gps = pd.DataFrame(team1[['lat', 'lon']])
      st.map(gps, zoom=11)

      #st.subheader("Sample 2 - Team A - 2021/07/03")
      #gps = pd.DataFrame(team1[['lat', 'lon']])
      #st.map(gps, zoom=11)

      #st.subheader("Sample 3 - Team B - 2020/03/22")
      #gps = pd.DataFrame(team1[['lat', 'lon']])
      #st.map(gps, zoom=11)

      #st.subheader("Sample 4 - Team B - 2021/07/07")
      #gps = pd.DataFrame(team1[['lat', 'lon']])
      #rst.map(gps, zoom=11)

   with tab3: # --- ANALYSIS ---

   
# --- Selection box 1 ---
      box = st.selectbox('1- Select which dataset you want to visualize the random sample', ["TeamA_2020_2d44f941", "TeamB_2020_4405bb1f", 'TeamA_2021_af719df9','TeamB_2021_29c5271b'])
      #st.markdown("OR")
# Selection box 2
      #date = st.date_input("1- Select which date you want to visualize (01.06.2020 - 30.12.2021) > WORK IN PROGRESS",datetime.date(2020, 6, 1))
      
# Sample size picking analyse 1
      slider_analyse_1 = st.slider('2- Select the number of random rows', min_value=5, max_value=50, value=5, step=10)
      
# Radio button selection
      genre = st.radio("3- Select your favorite vizualisation",('Line plot','Bar plot','Scatter plot'))

# Plot color selection
      color = st.color_picker('4- Pick a color for your plot by clicking on the box', '#0034F9')
      
# Plot_1_TeamA_2020
      if box == "TeamA_2020_2d44f941" :
         st.header("Heart rate over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            plot= st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            plot = st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            plot = st.plotly_chart(fig, use_container_width=True)  

# Plot_2_TeamA_2020
      if box == "TeamA_2020_2d44f941" :
         st.header("Acceleration over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

# Plot_3_TeamA_2020
      if box == "TeamA_2020_2d44f941" :
         st.header("Rotation over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)    
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

# Plot_1_TeamA_2021
      if box == "TeamA_2021_af719df9":
         st.header("Heart rate over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_2_TeamA_2021
      if box == "TeamA_2021_af719df9":
         st.header("Heart rate over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_3_TeamA_2021
      if box == "TeamA_2021_af719df9":
         st.header("Heart rate over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)



# Plot_1_TeamB_2020  
      if box == "TeamB_2020_4405bb1f":
         st.header("Heart rate over Time - Team B")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_2_TeamB_2020
      if box == "TeamB_2020_4405bb1f" :
         st.header("Acceleration over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)    
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

# Plot_3_TeamB_2020
      if box == "TeamB_2020_4405bb1f" :
         st.header("Rotation over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 



# Plot_1_TeamB_2021
      if box == "TeamB_2021_29c5271b":
         st.header("Heart rate over Time - Team B")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)  
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)  
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_2_TeamB_2021
      if box == "TeamB_2021_29c5271b" :
         st.header("Acceleration over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

# Plot_3_TeamB_2021
      if box == "TeamB_2021_29c5271b" :
         st.header("Rotation over Time - Team A")
         if genre == 'Line plot':
            fig = px.line((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)
         elif genre == 'Bar plot':
            fig = px.bar((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)    
         elif genre == 'Scatter plot':
            fig = px.scatter((team1.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

   with tab4: #--- 3D_GPS_MAP ---

      #3d plot

      fig = px.line_3d(team1, x='lon', y='lat', z='time',color='player_name')#, animation_frame="time",animation_group="player_name")
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
      fig = px.scatter(team1, x='lon', y='lat',color='player_name', animation_frame="time",animation_group="player_name", width=1009, height=750)#color_discrete_sequence=['red', 'cornflowerblue'],width=1009, height=811
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
      image_filename = 'D:/Simula/Git 2023/soccer-dashboard/data/gps/Football.png'
      plotly_logo = base64.b64encode(open(image_filename, 'rb').read())

      #Add picture in background
      fig.update_layout(images= [dict(source='data:image/png;base64,{}'.format(plotly_logo.decode()),xref="paper", yref="paper"
         ,x=0, y=1,sizex=1, sizey=1,layer="below",opacity=0.75,)])
                    #xanchor="left",
                    #yanchor="top",
                    #sizing="stretch",
      

      st.plotly_chart(fig)
                   