import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime
import mysql.connector
from contextlib import contextmanager
 
@contextmanager
def closing(connection):
    try:
        yield connection
    finally:
        connection.close()

@st.cache_resource
def init_connection():
    toml_data = st.secrets["mysql"]
    HOST_NAME = toml_data['host']
    DATABASE = toml_data['database']
    PASSWORD = toml_data['password']
    USER = toml_data['user']
    PORT = toml_data['port']
    conn = mysql.connector.connect(host=HOST_NAME, database=DATABASE, user=USER, passwd=PASSWORD, use_pure=True)
    return conn

conn = init_connection()

def run_query(query):
    with closing(conn.cursor()) as cur:
        cur.execute(query)
        return cur.fetchall()

rowA = "SELECT count(distinct(year(date))) FROM daily_features where player_name like 'TeamA%';"
rowB = "SELECT count(distinct(year(date))) FROM daily_features where player_name like 'TeamB%';"
inj = 'select distinct(player_name) Player, severity TypeOfInjury from injuries group by Player;'
ses_fet = 'select distinct(Player_name) Player_name, `Total_distance`, `Top_speed`, `Duration` from LH_session;'
dataset = "SELECT * FROM gps ORDER BY date, time ASC"
df_team_A = "SELECT * FROM gps WHERE player_name LIKE 'TeamA%' "
df_team_B = "SELECT * FROM gps WHERE player_name LIKE 'TeamB%' "
daily_features = "SELECT * FROM daily_features"
gps = 'select distinct(Player_name) Player_name, Start_time, End_time, Lat_start, Lon_start, Lat_end, Lon_end from LH_HIR;'
