import streamlit as st

def homepage():
    st.set_page_config(
        page_title="Soccer Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="auto",
    )

    with open('README.md', 'r',encoding='utf-8') as file:
        descrip = file.read()
    # get the first section of the README file
    descrip = str(descrip)
    index_1 = descrip.index('# Soccer Dashboard')
    index_2 = descrip.index('\n#')
    section = descrip[index_1:index_2]
    # show a different title
    section = section.replace('# Soccer Dashboard','')
    st.title('Welcome to the Soccer Dashboard')
    st.markdown(section)

homepage()

