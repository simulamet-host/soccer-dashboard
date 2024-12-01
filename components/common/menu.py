import streamlit as st

def menu():
    # define the pages and their paths, and sub-pages if any
    pages = {
        "🏠 Homepage": {
            "path": "homepage.py",
        },
        "🌍 GPS": {
            "path": "pages/gps__sprints.py",
            "sub_pages": {
                'Sprints': "pages/gps__sprints.py",
                'Overall Mobility': "pages/gps__mobility.py",
            }
        },
        "💉 Injuries - Objective": {
            "path": "pages/injuries_objective__overview.py",
            "sub_pages": {
                'Overview': "pages/injuries_objective__overview.py",
                'Analysis': "pages/injuries_objective__analysis.py",
            }
        },
        "🗃️ Other": {
            "path": "pages/other__dataset_overview.py",
            "sub_pages": {
                'Dataset Overview': "pages/other__dataset_overview.py",
                'Game Performance': "pages/other__game_performance.py",
                'Illnesses': "pages/other__illnesses.py",
                "Injuries - Subjective": "pages/other__injuries.py",
                'Training Load': "pages/other__training_load.py",
                'Wellness': "pages/other__wellness.py",
            }
        },
    }

    # display the menu in the sidebar
    for page in pages:
        st.sidebar.page_link(pages[page]["path"], label=page)
        if "sub_pages" in pages[page]:
            for sub_page in pages[page]["sub_pages"]:
                path = pages[page]["sub_pages"][sub_page]
                label = "  ➤ " + sub_page
                st.sidebar.page_link(path, label=label)
