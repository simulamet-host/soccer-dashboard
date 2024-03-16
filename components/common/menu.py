import streamlit as st

def menu(sub_pages: dict = None):
    # main pages
    main_pages = {
        "Homepage": "homepage.py",
        "Dataset Overview": "pages/dataset_overview.py",
        "Player View": "pages/player_view.py",
        "Team View": "pages/team_view.py",
        "Researcher View": "pages/researcher_view.py"
    }

    for page in main_pages:
        st.sidebar.page_link(main_pages[page], label=page)

    # sub pages if any
    if sub_pages:
        st.sidebar.divider()
        for page in sub_pages:
            st.sidebar.page_link(sub_pages[page], label=page)
