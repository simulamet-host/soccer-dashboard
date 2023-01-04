import pandas as pd
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import datetime
import numpy as np
from pathlib import Path
import sys

#sys.path.append(str(Path(__file__).parent.parent))

# cache
@st.experimental_memo 
  
def load_data1(path_to_data: Path):
    data1 = pd.read_parquet(Path) 
    return data1

def get_data2(df_B_20):
    data2 = pd.read_parquet(df_B_20) 
    return data2

def get_data3(df_A_21):
    data3 = pd.read_parquet(df_A_21)
    return data3

def get_data4(df_B_21):
    data4 = pd.read_parquet(df_B_21) 
    return data4

def get_data5(df_A_20):
    data5 = pd.read_csv(board_players) 
    return data5


#df_A_20 = pd.read_parquet(r"C:\Users\hensl\Documents\GitHub\soccer-dashboard\data\gps\2020-06-01-TeamA-2d44f941.parquet").sample(15).sort_values(by="time")
#df_B_20 = pd.read_parquet(r"C:\Users\hensl\Documents\GitHub\soccer-dashboard\data\gps\2020-07-03-TeamB-4405bb1f.parquet").sample(15).sort_values(by='time')
#df_A_21 = pd.read_parquet(r"C:\Users\hensl\Documents\GitHub\soccer-dashboard\data\gps\2021-03-22-TeamA-af719df9.parquet").sample(15).sort_values(by='time')
#df_B_21 = pd.read_parquet(r"C:\Users\hensl\Documents\GitHub\soccer-dashboard\data\gps\2021-07-07-TeamB-29c5271b.parquet").sample(15).sort_values(by='time')

df_A_20 = Path(__file__).parent.parent / "data" / "gps" / "2020-06-01-TeamA-2d44f941.parquet"
df_B_20 = Path(__file__).parent.parent / "data" / "gps" / "2020-07-03-TeamB-4405bb1f.parquet"
df_A_21 = Path(__file__).parent.parent / "data" / "gps" / "2021-03-22-TeamA-af719df9.parquet"
df_B_21 = Path(__file__).parent.parent / "data" / "gps" / "2021-07-07-TeamB-29c5271b.parquet"


board_players = Path(__file__).parent.parent / "data" / "gps" / "board_players.csv"

#board_players = pd.read_csv (r"C:\Users\hensl\Documents\GitHub\soccer-dashboard\data\gps\board_players.csv")

    #def get_data(filename):
    #taxi_data = pd.read_parquet(filename)
    #return taxi_data

    #taxi_data = get_data('data/taxi_data.parquet')

def gps_statistics():
   
   st.title("GPS Information")

   tab1, tab2, tab3= st.tabs(["Raw Data ", "Map Visualization", "Analysis"])

   with tab1:

      st.header("Sample 1 - Team A - 2020/06/01")
      #data1 = get_data1(Path(__file__).parent.parent/"data"/"gps"/"2020-06-01-TeamA-2d44f941.parquet")
      #path_to_gps = Path(__file__).parent.parent / "data" / "gps" / "2020-06-01-TeamA-2d44f941.parquet"
      #dataset = load_data1("path_to_gps")
      #st.dataframe(dataset)

      st.header("Sample 2 - Team A - 2021/07/03")
      #st.dataframe(get_data2)

      st.header("Sample 3 - Team B - 2020/03/22")
      #st.dataframe(get_data3)

      st.header("Sample 4 - Team B - 2021/07/07")
      #st.dataframe(get_data4)

   with tab2:
      
      st.subheader("Sample 1 - Team A - 2020/06/01")
      #gps = pd.DataFrame(data1[['lat', 'lon']])
      st.map()

      st.subheader("Sample 2 - Team A - 2021/07/03")
      #gps = pd.DataFrame(df_A_21[['lat', 'lon']])
      st.map()   #(gps, zoom=11)

      st.subheader("Sample 3 - Team B - 2020/03/22")
      #gps = pd.DataFrame(df_B_20[['lat', 'lon']])
      st.map()    #(gps, zoom=11)

      st.subheader("Sample 4 - Team B - 2021/07/07")
      #gps = pd.DataFrame(df_B_21[['lat', 'lon']])
      st.map() #(gps, zoom=11)

   with tab3:

      st.header("Settings")

      box = st.selectbox('1-Select which dataset you want to visualize :', ["TeamA-2d44f941", "TeamB-4405bb1f", 'TeamA-af719df9','TeamB-29c5271b'])
      st.markdown("OR")
      date = st.date_input("1-Select which date you want to visualize (01.01.2020 - 30.12.2021):",datetime.date(2020, 1, 1))
      st.markdown("")
      genre = st.radio("2-What's your favorite plot ?",('Bar plot', 'Line plot', 'Scatter plot'))


      if genre == 'Bar plot':
         st.write('')
      elif genre == 'Line plot':
         st.write('')
      elif genre == 'Scatter plot':
         st.write('')
      else:
         st.write("")


      color = st.color_picker('3-Pick a color for your plot', '#00f900')
      
      heading_heart_rate = "Heart rate vs Time"
      
      if box == "TeamA_2020" :
         st.header(heading_heart_rate)
         #fig = px.line(df_A_20, x='time', y='heart_rate')
         #st.plotly_chart(fig, use_container_width=True)
         

      elif box == "TeamA_2021":
           st.header(heading_heart_rate)
           #fig = px.line(df_A_21, x='time', y='heart_rate')
           #st.plotly_chart(fig, use_container_width=True)

      elif "TeamB_2020" in box:
           st.header(heading_heart_rate)
           #fig = px.line(df_B_20, x='time', y='heart_rate')
           #st.plotly_chart(fig, use_container_width=True)

      else :
           st.header(heading_heart_rate)
           #fig = px.line(df_B_21, x='time', y='heart_rate')
           #st.plotly_chart(fig, use_container_width=True)
   
      st.header("Number of sample")
      #st.dataframe (board_players, use_container_width=True)






      
   