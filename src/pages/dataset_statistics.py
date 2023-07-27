import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime
import src.utils.queries as qu
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

conn = qu.conn

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
      df = pd.read_sql(qu.daily_features, conn)
      gb = GridOptionsBuilder.from_dataframe(df)
      gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
      gb.configure_side_bar() #Add a sidebar
      gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
      gridOptions = gb.build()

      grid_response = AgGrid(
         df,
         gridOptions=gridOptions,
         data_return_mode='AS_INPUT', 
         update_mode='MODEL_CHANGED', 
         fit_columns_on_grid_load=True,
         theme='streamlit',
         enable_enterprise_modules=True,
         height=350, 
         width='100%',
         reload_data=True
      )

      data = grid_response['data']
      selected = grid_response['selected_rows'] 
      df = pd.DataFrame(selected)
      #rowA = qu.run_query(qu.rowA)
      #rowB = qu.run_query(qu.rowB)

      #data = {
      #  "Team Name": ["TeamA", "TeamB"],
      #  "Number of Years": [int(rowA[0][0]), int(rowB[0][0])]
      #}
      
      #df = pd.DataFrame(data)
        
      hide_dataframe_row_index = """
        <style>
        .row_heading.level0 {display:none}
        .blank {display:none}
        </style>
        """
    
      st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

      #st.table(df)

   with tab4:
      st.header("Game Performance")
      df = pd.DataFrame(columns=["Game Performance"])
      st.table(df)

   with tab5:
      st.header("GPS")
      df = pd.read_sql(qu.gps, conn)
      gb = GridOptionsBuilder.from_dataframe(df)
      gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
      gb.configure_side_bar() #Add a sidebar
      gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
      gridOptions = gb.build()

      grid_response = AgGrid(
         df,
         gridOptions=gridOptions,
         data_return_mode='AS_INPUT', 
         update_mode='MODEL_CHANGED', 
         fit_columns_on_grid_load=True,
         theme='streamlit',
         enable_enterprise_modules=True,
         height=350, 
         width='100%',
         reload_data=True
      )

      data = grid_response['data']
      selected = grid_response['selected_rows'] 
      df = pd.DataFrame(selected)
      #df = pd.DataFrame(columns=['GPS'])
      #st.table(df)

   with tab6:
      st.header("Illnesses")
      df = pd.DataFrame(columns=['Illnesses'])
      st.table(df)
      
   with tab7:
      st.header("Injuries")
      #df = pd.DataFrame(columns=['Injuries'])
      df = pd.read_sql(qu.inj, conn)
      gb = GridOptionsBuilder.from_dataframe(df)
      gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
      gb.configure_side_bar() #Add a sidebar
      gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
      gridOptions = gb.build()

      grid_response = AgGrid(
         df,
         gridOptions=gridOptions,
         data_return_mode='AS_INPUT', 
         update_mode='MODEL_CHANGED', 
         fit_columns_on_grid_load=False,
         theme='streamlit',
         enable_enterprise_modules=True,
         height=350, 
         width='100%',
         reload_data=True
      )

      data = grid_response['data']
      selected = grid_response['selected_rows'] 
      df = pd.DataFrame(selected)
      #st.table(df)      

   with tab8:
      st.header("Session Features")
      #df = pd.DataFrame(columns=['Session Features'])
      df = pd.read_sql(qu.ses_fet, conn)
      #st.table(df)                                                            

      gb = GridOptionsBuilder.from_dataframe(df)
      gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
      gb.configure_side_bar() #Add a sidebar
      gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
      gridOptions = gb.build()

      grid_response = AgGrid(
         df,
         gridOptions=gridOptions,
         data_return_mode='AS_INPUT', 
         update_mode='MODEL_CHANGED', 
         fit_columns_on_grid_load=False,
         theme='streamlit',
         enable_enterprise_modules=True,
         height=350, 
         width='100%',
         reload_data=True
      )

      data = grid_response['data']
      selected = grid_response['selected_rows'] 
      df = pd.DataFrame(selected)
