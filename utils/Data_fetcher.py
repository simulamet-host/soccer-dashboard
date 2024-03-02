import streamlit as st

# fetch data from mysql database and return the data
def fetch_from_mysql(table: str, columns: list):
    # initialize connection
    conn = st.connection('mysql', type='sql')

    # query the database
    df = conn.query(f'SELECT {", ".join(columns)} FROM {table}')

    return df

# fetch data and return the data
# can choose from various sources; default is mysql
def fetch_data(table: str, columns: list, source: str = 'mysql'):
    if source == 'mysql':
        return fetch_from_mysql(table, columns)
    else:
        raise ValueError('Source not supported')
