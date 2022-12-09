import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime


def dataset_statistics():
   
   st.set_page_config(page_title='Dataset Statistics')
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
      df = pd.DataFrame(columns=['Daily Features'])
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
