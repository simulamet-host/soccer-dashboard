import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime
import mysql.connector


@st.experimental_singleton
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

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rowA = "SELECT count(distinct(year(date))) FROM daily_features where player_name like 'TeamA%';"
rowB = "SELECT count(distinct(year(date))) FROM daily_features where player_name like 'TeamB%';"
inj = 'select distinct(player_name) Player, severity TypeOfInjury from injuries group by Player;'
ses_fet = 'select distinct(Player) Player, `Distance (m)`, `Top speed (m/s^2)`, `Duration (s)` from LH_HIR_features;'
