import streamlit as st

def menu():
    # define the pages and their paths, and sub-pages if any
    pages = {
        "Homepage": {
            "path": "homepage.py",
        },
        "Dataset Overview": {
            "path": "pages/dataset_overview.py",
            "sub_pages": {
                'Game Performance': "pages/dataset_overview_game_performance.py",
                'Illnesses': "pages/dataset_overview_illnesses.py",
                "Injuries": "pages/dataset_overview_injuries.py",
                'Training Load': "pages/dataset_overview_training_load.py",
                'Wellness': "pages/dataset_overview_wellness.py",
            }
        },
        "Analysis": {
            "path": "pages/analysis.py",
            "sub_pages": {
                'Game Performance': "pages/analysis_game_performance.py",
                'Illnesses': "pages/analysis_illnesses.py",
                "Injuries": "pages/analysis_injuries.py",
                "Injuries - Finn": "pages/analysis_injuries_finn.py",
                'Training Load': "pages/analysis_training_load.py",
                'Wellness': "pages/analysis_wellness.py",
                'GPS': "pages/analysis_gps.py",
            }
        }
    }

    # display the menu in the sidebar
    for page in pages:
        st.sidebar.page_link(pages[page]["path"], label=page)
        if "sub_pages" in pages[page]:
            for sub_page in pages[page]["sub_pages"]:
                path = pages[page]["sub_pages"][sub_page]
                label = " • " + sub_page
                st.sidebar.page_link(path, label=label)
