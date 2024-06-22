import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection

# fetch data from mysql database and return the data
@st.cache_data()
def fetch_from_mysql(table: str, columns: list, where: str = None, limit: int = None):
    '''
    Fetch data from a MySQL database and return the data as a pandas DataFrame.

    Parameters:
    table (str): name of the table to fetch data from
    columns (list): list of columns to fetch, e.g. ['column1', 'column2'], or ['*'] to fetch all columns
    where (str): where clause to filter the data; default is None
    limit (int): limit the number of rows to fetch; default is None

    Returns:
    df (pd.DataFrame): fetched data
    '''
    # initialize connection
    conn = st.connection('mysql', type='sql')

    # query the database
    limit_str = f'LIMIT {limit}' if limit else ''
    query = f'SELECT {", ".join(columns)} FROM `{table}` {where} {limit_str}'
    df = conn.query(query)

    return df

# fetch data and return the data
# can choose from various sources; default is mysql
@st.cache_data()
def fetch_data(table: str, columns: list, source: str = 'mysql', where: str = None, limit: int = None):
    if source == 'mysql':
        return fetch_from_mysql(table, columns, where=where, limit=limit)
    else:
        raise ValueError('Source not supported')

@st.cache_data()
def read_gc_file(
    file: str,
    input_format: str or None = None,
    ttl: int or None = None
):
    '''
    Read a file from Google Cloud Storage and return the content.
    See https://github.com/streamlit/files-connection?tab=readme-ov-file#read for details
    '''
    conn = st.connection('gcs', type=FilesConnection)
    content = conn.read(file, input_format, ttl)
    return content

@st.cache_resource
def open_gc_file(
    file: str,
    mode: str = 'rb',
    *args,
    **kwargs
):
    '''
    Open a file from Google Cloud Storage and return the file object.
    See https://github.com/streamlit/files-connection?tab=readme-ov-file#open and https://filesystem-spec.readthedocs.io/en/latest/api.html#fsspec.spec.AbstractFileSystem.open for details
    '''
    conn = st.connection('gcs', type=FilesConnection)
    file_obj = conn.open(file, mode, *args, **kwargs)
    return file_obj

@st.cache_data()
def read_gc_csv(
    file: str,
    sep: str = ',',
    encoding: str = 'utf-8',
    *args,
    **kwargs
):
    '''
    Read a CSV file from Google Cloud Storage and return the content as a pandas DataFrame.
    st.connection.read() was supposed to do this, but it has encoding issues, so I have to use this workaround.
    '''
    conn = st.connection('gcs', type=FilesConnection)
    file_obj = conn.open(file, mode='r', encoding=encoding, *args, **kwargs)
    df = pd.read_csv(file_obj, sep=sep)
    return df
