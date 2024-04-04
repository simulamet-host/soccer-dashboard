import streamlit as st

# fetch data from mysql database and return the data
@st.cache_data()
def fetch_from_mysql(table: str, columns: list):
    '''
    Fetch data from a MySQL database and return the data as a pandas DataFrame.

    Parameters:
    table (str): name of the table to fetch data from
    columns (list): list of columns to fetch, e.g. ['column1', 'column2'], or ['*'] to fetch all columns

    Returns:
    df (pd.DataFrame): fetched data
    '''
    # initialize connection
    conn = st.connection('mysql', type='sql')

    # query the database
    df = conn.query(f'SELECT {", ".join(columns)} FROM {table}')

    return df

# fetch data and return the data
# can choose from various sources; default is mysql
@st.cache_data()
def fetch_data(table: str, columns: list, source: str = 'mysql'):
    if source == 'mysql':
        return fetch_from_mysql(table, columns)
    else:
        raise ValueError('Source not supported')
