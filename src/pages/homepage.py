from pathlib import Path
import streamlit as st
import sys
import os
import pickle
import time

# Define the main page function
def homepage(): 
    with open('README.md', 'r',encoding='utf-8') as file:
        descrip = file.read()
    descrip = str(descrip)
    index_1 = descrip.index('# Soccer Dashboard')
    index_2 = descrip.index('## ')
    st.markdown("## Welcome to the Soccer Dashboard")
    st.markdown(descrip[index_1:index_2])