import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime
import mysql.connector
import toml


toml_data = st.secrets["mysql"]
HOST_NAME = toml_data['host']
DATABASE = toml_data['database']
PASSWORD = toml_data['password']
USER = toml_data['user']
PORT = toml_data['port']
conn = mysql.connector.connect(host=HOST_NAME, database=DATABASE, user=USER, passwd=PASSWORD, use_pure=True)

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def dataset_statistics():
   
   st.title('Dataset Statistics')
   st.markdown("## Dataset Statistics")

   tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Overview", "Missing Data", "Daily Features", "Game Performance", "GPS", "Illnesses", "Injuries", "Session Features"])

   with tab1:
      st.header("Overview")
      df = pd.DataFrame(columns=['Team', 'Number of players', 'Number of years', 'Number of samples'])
      st.table(df)

   with tab2:
      st.header("Missing Data")
      df = pd.DataFrame(columns=['Missing Data'])
      st.table(df)

   with tab3:
      st.header("Daily Features")
      rowA = run_query("SELECT count(distinct(year(date))) FROM daily_features where player_name like 'TeamA%';")
      rowB = run_query('''SELECT count(distinct(year(date))) FROM daily_features where player_name like "TeamB%";''')

      data = {
        "Team Name": ["TeamA", "TeamB"],
        "Number of Years": [int(rowA[0][0]), int(rowB[0][0])]
      }
      df = pd.DataFrame(data)
      st.table(df)

   with tab4:
      st.header("Game Performance")
      df = pd.DataFrame(columns=["Game Performance"])
      st.table(df)

   with tab5:
      st.header("GPS")
      df = pd.DataFrame(columns=['GPS'])
      st.table(df)

   with tab6:
      st.header("Illnesses")
      df = pd.DataFrame(columns=['Illnesses'])
      st.table(df)
   with tab7:
      st.header("Injuries")
      df = pd.DataFrame(columns=['Injuries'])
      st.table(df)      

   with tab8:
      st.header("Session Features")
      df = pd.DataFrame(columns=['Session Features'])
      st.table(df)                                                            
