import streamlit as st

pages = [
    st.Page("page_input.py", title="User Schedules"),
    st.Page("page_output.py", title="Generate Calender")
]

pg = st.navigation(pages)
pg.run()