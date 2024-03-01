import streamlit as st

# fetch data from mysql database and return the data
def fetch_from_mysql(table_name: str, columns: list):
    # initialize connection
    conn = st.connection('mysql', type='sql')

    # query the database
    df = conn.query(f'SELECT {", ".join(columns)} FROM {table_name}')

    return df
