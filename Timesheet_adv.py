
import streamlit as st
from datetime import datetime, time, timedelta
### nedd to change to get day or date based on current week and witj syncronization.

st.title("🕒 Weekly Timesheet Entry")

# Sample days of the week
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

st.markdown("### Enter your hours")

# Table-like header row
header_cols = st.columns([1, 2, 3, 2, 2, 2])
header_cols[0].markdown("**Day**")
header_cols[1].markdown("**Date**")
header_cols[2].markdown("**Project**")
header_cols[3].markdown("**Start Time**")
header_cols[4].markdown("**End Time**")
header_cols[5].markdown("**Total Hours**")

# Store input values
timesheet_entries = []

for i in range(len(days)):
    row = st.columns([1, 2, 3, 2, 2, 2])

    day = days[i]
    row[0].markdown(f"**{day}**")
    date = row[1].date_input(f"date_{i}", label_visibility="collapsed", value=datetime.today() + timedelta(days=i))
    project = row[2].text_input(f"project_{i}", label_visibility="collapsed", placeholder="e.g. Client ABC")
    start_time = row[3].time_input(f"start_{i}", label_visibility="collapsed", value=time(9, 0))
    end_time = row[4].time_input(f"end_{i}", label_visibility="collapsed", value=time(17, 0))

    # Compute total hours
    total_hours = (datetime.combine(datetime.today(), end_time) - 
                   datetime.combine(datetime.today(), start_time)).seconds / 3600
    row[5].markdown(f"**{total_hours:.2f}**")

    # Store the row
    timesheet_entries.append({
        "Day": day,
        "Date": date,
        "Project": project,
        "Start Time": start_time,
        "End Time": end_time,
        "Total Hours": total_hours
    })

st.markdown("---")
if st.button("Submit Timesheet"):
    st.success("✅ Timesheet submitted!")
    st.write(timesheet_entries)  # or convert and save as CSV, send to DB, etc.
