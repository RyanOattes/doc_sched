import streamlit as st
from streamlit_calendar import calendar

import datetime

from algo import generate_schedule

st.set_page_config(layout="wide")

selected_year = st.selectbox("Pick a year", (2025, 2026, 2027), index=0)
selected_month = st.selectbox("Pick a month", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), index=datetime.datetime.now().month - 1)

run_now = st.button("Generate Schedule")
if run_now:
    with st.spinner(text="Generating Schedule", show_time=True):
        schedule_fillers, schedule_slots = generate_schedule(selected_year, selected_month)

        st.session_state["schedule_fillers"] = schedule_fillers
        st.session_state["schedule_slots"] = schedule_slots

if "schedule_fillers" in st.session_state:
    schedule_fillers = st.session_state["schedule_fillers"]
    schedule_slots = st.session_state["schedule_slots"]

    calendar_options = {
        "editable": False,
        "selectable": False,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "18:00:00",
        #"initialView": "resourceTimelineDay",
        "initialView": "dayGridMonth",
        #"resourceGroupField": "building",
        #"resources": [
        #    {"id": "a", "building": "Building A", "title": "Building A"},
        #    {"id": "b", "building": "Building A", "title": "Building B"},
        #    {"id": "c", "building": "Building B", "title": "Building C"},
        #    {"id": "d", "building": "Building B", "title": "Building D"},
        #    {"id": "e", "building": "Building C", "title": "Building E"},
        #    {"id": "f", "building": "Building C", "title": "Building F"},
        #],
        "resourceGroupField": "id",
        "resources": [
            {"id": "benny.oattes@kobai.io"},
            {"id": "pearl.oattes@kobai.io"}
        ]
    }
    calendar_events = []
    for i, s in enumerate(schedule_slots):
        case_mgr = schedule_fillers[i]["id"] 
        doc = schedule_slots[i]["user_name"]
        date_string = schedule_slots[i]["date"].strftime("%Y-%m-%d")
        if schedule_slots[i]["slot"] == "Morning":
            start_time_string = date_string + "T09:00:00"
            end_time_string = date_string + "T12:00:00"
        else:
            start_time_string = date_string + "T13:00:00"
            end_time_string = date_string + "T16:00:00"
        calendar_events.append(
            {
                "title": case_mgr + " with " + doc,
                "start": start_time_string,
                "end": end_time_string,
                "resourceId": doc
            }
        )
    custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """

    calendar = calendar(
        events=calendar_events,
        options=calendar_options,
        #custom_css=custom_css,
        key='calendar', # Assign a widget key to prevent state loss
        )
    st.write(calendar)