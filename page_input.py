import datetime
import calendar
import streamlit as st

from database import init_schema, add_period, check_period_exists, get_periods, delete_period, get_users

st.set_page_config(layout="wide")

#########################
# State Management
#########################

if "init" not in st.session_state:
    st.session_state["init"] = True
    init_schema()

user_list = get_users()
user_options = []
for u in user_list:
    user_options.append(u["last_name"] + ", " + u["first_name"] + " (" + u["id"] + ")")
selected_user_option = st.selectbox("Pick a user", user_options)
selected_user_index = user_options.index(selected_user_option)
selected_user = user_list[selected_user_index]["id"]

selected_year = st.selectbox("Pick a year", (2025, 2026, 2027), index=0)
selected_month = st.selectbox("Pick a month", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), index=datetime.datetime.now().month - 1)


col1, col2, col3 = st.columns([1, 1, 1])
with col2:
#########################
# Data Entry Form
#########################

    min_date = datetime.date(selected_year, selected_month, 1)
    _, month_days = calendar.monthrange(selected_year, selected_month)
    max_date = datetime.date(selected_year, selected_month, month_days)

    st.write("Add dates you aren't available")

    selected_date = st.date_input("Pick a date", None, min_value=min_date, max_value=max_date)
    selected_slot = st.selectbox("Pick a time slot", ("Morning", "Afternoon", "All Day"), index=2)

    selected_period = {
        "date": selected_date, 
        "slot": selected_slot, 
        "user": selected_user,
        "year": selected_year,
        "month": selected_month,
        "type": "case_mgr_na"
        }

    select_now = st.button("Add a Period")
    if select_now:
        if selected_period["date"] is not None:
            #st.session_state["period_list"].append(selected_period)
            if not check_period_exists(selected_period):
                add_period(selected_period)

#########################
# Selected Period Output
#########################
with col1:
    #for period in st.session_state["period_list"]:
    for period in get_periods(selected_user, selected_year, selected_month):
        st.write(period["date"], period["slot"])


with col3:
    existing_periods = get_periods(selected_user, selected_year, selected_month)
    
    if len(existing_periods) > 0:
        deletable_items = []
        for p in existing_periods:
            deletable_items.append(p["date"].strftime('%Y-%m-%d') + " " + p["slot"])
        
        item_to_delete = st.selectbox("Pick a period", deletable_items)

        index_to_delete = deletable_items.index(item_to_delete)

        period_to_delete = existing_periods[index_to_delete]

        delete_now = st.button("Delete")
        if delete_now:
            #print(period_to_delete)
            delete_period(period_to_delete)
            st.rerun()