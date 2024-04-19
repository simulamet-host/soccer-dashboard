import streamlit as st

def menu(sub_pages: dict = None, position: int = -1):
    main_pages = {
        "Homepage": "homepage.py",
        "Dataset Overview": "pages/dataset_overview.py",
        "Player View": "pages/player_view.py",
        "Team View": "pages/team_view.py",
        "Researcher View": "pages/researcher_view.py"
    }

    # if sub_pages is not provided, or position is not valid, display all the main pages
    if not sub_pages or position < 0 or position >= len(main_pages):
        for page in main_pages:
            st.sidebar.page_link(main_pages[page], label=page)
    else:
        # display the main pages before the position
        for page in list(main_pages.keys())[:position]:
            st.sidebar.page_link(main_pages[page], label=page)

        # sub pages
        for page in sub_pages:
            # prefix the page label to indicate that it's a sub page
            label = f" • {page}"
            st.sidebar.page_link(sub_pages[page], label=label)

        # rest of the main pages
        for page in list(main_pages.keys())[position:]:
            st.sidebar.page_link(main_pages[page], label=page)
