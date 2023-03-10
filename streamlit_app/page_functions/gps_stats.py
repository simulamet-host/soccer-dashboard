import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager

import streamlit as st
import pyarrow as pa

import missingno as msno
import plotly.express as px
import datetime
import numpy as np
   
# cache
#@st.cache_data
#def load_data(path_to_gps: Path):
    #return pickle.load(open(path_to_gps, "rb"))

#path_to_gps = Path(__file__).parent.parent / "data" / "gps" / "2020-06-01-TeamA-2d44f941.parquet"

# Load full dataset with a max sample size of 50
df_A_20 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2020-06-01-TeamA-2d44f941.parquet").sample(50).sort_values(by="time")
df_B_20 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2020-07-03-TeamB-4405bb1f.parquet").sample(50).sort_values(by='time')
df_A_21 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2021-03-22-TeamA-af719df9.parquet").sample(50).sort_values(by='time')
df_B_21 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2021-07-07-TeamB-29c5271b.parquet").sample(50).sort_values(by='time')

# Load only one column of the full dataset for counting purposes and lower memory use
df_1 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2020-06-01-TeamA-2d44f941.parquet", columns=['player_name'])
df_2 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2020-07-03-TeamB-4405bb1f.parquet", columns=['player_name'])
df_3 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2021-03-22-TeamA-af719df9.parquet", columns=['player_name'])
df_4 = pd.read_parquet(r"D:\Simula\Git 2022\soccer-dashboard\data\gps\2021-07-07-TeamB-29c5271b.parquet", columns=['player_name'])

#df_A_20 = df_A1_20.sample(slider_number1).sort_values(by="time")
#df_B_20 = df_B2_20.sample(slider_number2).sort_values(by="time")
#df_A_21 = df_A1_21.sample(slider_number3).sort_values(by="time")
#df_B_21 = df_B2_21.sample(slider_number4).sort_values(by="time")

def gps_statistics():
   
   st.title("GPS Information")

   tab1, tab2, tab3, tab4, tab5= st.tabs(["Raw data ", "Map visualization", "Analysis", "3d Map visualization", "2d Map visualization"])

   with st.sidebar:
      st.selectbox("Select Team",[("Team A", "TeamA"), ("Team B", "TeamB")],format_func=lambda x: x[0],)
      st.selectbox("Select Player","player_names")#,format_func=lambda x: x[0],)

   with tab1: #Raw data

      st.markdown("")
      # Metric - no Dataframe accepted
      col1, col2, col3, col4 = st.columns(4)
      col1.metric("Total number of rows", len(df_1)),#('TeamA-2d44f941')) # Metric

      st.markdown("")
      
      # Dataset sample board 1
      st.header("Dataset details")
      st.dataframe(df_A_20.describe().T)
      st.title("")

      # Dataset sample board 1
      st.header("Sample of 50 rows")
      st.dataframe(df_A_20)#.iloc)[0:slider_number1])
      st.title("")
      
      # Plot sample board 1 missing data
      st.markdown("")
      st.header("Missing data")
      miss = msno.matrix(df_A_20)
      st.pyplot(miss.figure)

      # Plot sample board 1 zero data

      st.markdown("")
      st.header("Zero data")
      for column_name in df_A_20:
         column = df_A_20[column_name]
         count = (column == 0).value_counts()
         st.table (count)        
          #df = pd.DataFrame(count)


   with tab2: #Map visualization
      
      st.subheader("Sample 1 - Team A - 2020/06/01")
      gps = pd.DataFrame(df_A_20[['lat', 'lon']])
      st.map(gps, zoom=11)

      st.subheader("Sample 2 - Team A - 2021/07/03")
      gps = pd.DataFrame(df_A_21[['lat', 'lon']])
      st.map(gps, zoom=11)

      st.subheader("Sample 3 - Team B - 2020/03/22")
      gps = pd.DataFrame(df_B_20[['lat', 'lon']])
      st.map(gps, zoom=11)

      st.subheader("Sample 4 - Team B - 2021/07/07")
      gps = pd.DataFrame(df_B_21[['lat', 'lon']])
      st.map(gps, zoom=11)


   with tab3: #Analysis

      st.markdown("")

# Selection box 1
      box = st.selectbox('1- Select which dataset you want to visualize the random sample', ["TeamA_2020_2d44f941", "TeamB_2020_4405bb1f", 'TeamA_2021_af719df9','TeamB_2021_29c5271b'])
      st.markdown("OR")
# Selection box 2
      date = st.date_input("1- Select which date you want to visualize (01.06.2020 - 30.12.2021) > WORK IN PROGRESS",datetime.date(2020, 6, 1))
      st.markdown("")

# Sample size picking analyse 1
      slider_analyse_1 = st.slider('2- Select the number of random rows', min_value=5, max_value=50, value=5, step=10)
      st.markdown("")

# Radio button selection
      genre = st.radio("3- Select your favorite vizualisation",('Bar plot', 'Line plot', 'Scatter plot'))

# Plot color selection
      color = st.color_picker('4- Pick a color for your plot by clicking on the box', '#0034F9')
      
# Plot_1_TeamA_2020
      if box == "TeamA_2020_2d44f941" :
         st.header("Heart rate over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_A_20.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_A_20.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_A_20.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)  

# Plot_2_TeamA_2020
      if box == "TeamA_2020_2d44f941" :
         st.header("Acceleration over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_A_20.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_A_20.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_A_20.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

# Plot_3_TeamA_2020
      if box == "TeamA_2020_2d44f941" :
         st.header("Rotation over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_A_20.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_A_20.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_A_20.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 



# Plot_1_TeamA_2021
      if box == "TeamA_2021_af719df9":
         st.header("Heart rate over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_2_TeamA_2021
      if box == "TeamA_2021_af719df9":
         st.header("Heart rate over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_3_TeamA_2021
      if box == "TeamA_2021_af719df9":
         st.header("Heart rate over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_A_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)



# Plot_1_TeamB_2020  
      if box == "TeamB_2020_4405bb1f":
         st.header("Heart rate over Time - Team B")
         if genre == 'Bar plot':
            fig = px.bar((df_B_20.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_B_20.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_B_20.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_2_TeamB_2020
      if box == "TeamB_2020_4405bb1f" :
         st.header("Acceleration over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_B_20.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_B_20.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_B_20.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

# Plot_3_TeamB_2020
      if box == "TeamB_2020_4405bb1f" :
         st.header("Rotation over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_B_20.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_B_20.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_B_20.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 



# Plot_1_TeamB_2021
      if box == "TeamB_2021_29c5271b":
         st.header("Heart rate over Time - Team B")
         if genre == 'Bar plot':
            fig = px.bar((df_B_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_B_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_B_21.iloc[0:slider_analyse_1]), x='time', y='heart_rate',size ="heart_rate",color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)

# Plot_2_TeamB_2021
      if box == "TeamB_2021_29c5271b" :
         st.header("Acceleration over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_B_21.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_B_21.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_B_21.iloc[0:slider_analyse_1]), x='time', y='accl_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

# Plot_3_TeamB_2021
      if box == "TeamB_2021_29c5271b" :
         st.header("Rotation over Time - Team A")
         if genre == 'Bar plot':
            fig = px.bar((df_B_21.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 
         elif genre == 'Line plot':
            fig = px.line((df_B_21.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True)   
         elif genre == 'Scatter plot':
            fig = px.scatter((df_B_21.iloc[0:slider_analyse_1]), x='time', y='gyro_x',color_discrete_sequence=[color])
            st.plotly_chart(fig, use_container_width=True) 

   with tab4: #3d_GPS_Map

      #3d plot
      st.markdown("")
      #3d = df_A_20['time','lat', 'lon']
      fig = px.scatter_3d(df_A_20, x='lon', y='lat', z='time',color='player_name')#, animation_frame="time",animation_group="player_name")
      fig.update_layout(yaxis_range=[63.4440,63.4460])
      fig.update_layout(xaxis_range=[10.4510,10.4530])
      #Marker update
      fig.update_traces(marker=dict(size=6,line=dict(width=2,color='black')),selector=dict(mode='markers'))
      st.plotly_chart(fig)

   with tab5: #2d_GPS_Map

      #2d plot with slider
      st.markdown("")
      fig = px.scatter(df_A_20, x='lon', y='lat',color='player_name',color_discrete_sequence=['red'], animation_frame="time",animation_group="player_name", opacity=1)
      #Resizing axes
      fig.update_layout(yaxis_range=[63.4440,63.4460])
      fig.update_layout(xaxis_range=[10.4510,10.4530])
      #Removing background lines
      fig.update_xaxes(showgrid=False, zeroline=False)
      fig.update_yaxes(showgrid=False, zeroline=False)
      #Marker update
      fig.update_traces(marker=dict(size=9,line=dict(width=2,color='black')),selector=dict(mode='markers'))
      #Set a local image as a background
      import base64
      image_filename = 'D:/Simula/Git 2023/soccer-dashboard/data/gps/football.jpg'
      plotly_logo = base64.b64encode(open(image_filename, 'rb').read())

      #Add picture in background
      fig.update_layout(images= [dict(source='data:image/png;base64,{}'.format(plotly_logo.decode()),xref="paper", yref="paper",x=0, y=1,sizex=1, sizey=1,layer="below")])
                    #xanchor="left",
                    #yanchor="top",
                    #sizing="stretch",
      st.plotly_chart(fig)

      # scatter plot animation with trailing lines/trace ?
                   