# Note: This script requires Streamlit to run. Ensure your environment supports Streamlit.

import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd

st.set_page_config(page_title="Time Card Calculator", layout="centered")

st.title("🕒 Time Card Calculator")
st.write("Select a date and enter your time entries. Supports both 24-hour (`14:30`) and 12-hour (`2:30 PM`) formats.")

# --- Initialize session state
if "time_entries" not in st.session_state:
    st.session_state.time_entries = {}

# --- Hourly rate
hourly_rate = st.number_input("Hourly pay rate ($):", min_value=0.0, step=0.5, value=20.0)

# --- Date selector
selected_date = st.date_input("Select a date", value=date.today())
day_of_week = selected_date.strftime("%A")

# --- Input for time
st.subheader(f"Enter Time for {day_of_week}, {selected_date.strftime('%B %d, %Y')}")

col1, col2, col3 = st.columns(3)
with col1:
    clock_in = st.text_input("Clock-in time", placeholder="e.g., 08:00 or 8:00 AM", key="in_time")
with col2:
    clock_out = st.text_input("Clock-out time", placeholder="e.g., 17:00 or 5:00 PM", key="out_time")

# --- Time parsing function
def parse_time(time_str):
    formats = ["%H:%M", "%I:%M %p"]
    for fmt in formats:
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except ValueError:
            continue
    return None

# --- Add entry
if col3.button("Add Entry"):
    start = parse_time(clock_in)
    end = parse_time(clock_out)
    if not start or not end:
        st.error("Invalid time format. Try HH:MM or HH:MM AM/PM.")
    elif end < start:
        st.error("Clock-out time must be after clock-in time.")
    else:
        duration = (end - start).total_seconds() / 3600
        date_str = selected_date.isoformat()
        if date_str not in st.session_state.time_entries:
            st.session_state.time_entries[date_str] = []
        st.session_state.time_entries[date_str].append({
            "Date": selected_date.strftime('%Y-%m-%d'),
            "Day": day_of_week,
            "Clock In": clock_in,
            "Clock Out": clock_out,
            "Hours": round(duration, 2)
        })
        st.success("Entry added!")

# --- Display entries
st.subheader("Time Entries")
total_hours = 0
entries_to_remove = []

for date_str in sorted(st.session_state.time_entries):
    entries = st.session_state.time_entries[date_str]
    if entries:
        st.markdown(f"### {date_str} ({entries[0]['Day']})")
        for i, entry in enumerate(entries):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"**Clock In:** {entry['Clock In']}")
            with col2:
                st.write(f"**Clock Out:** {entry['Clock Out']}")
            with col3:
                st.write(f"**Hours:** {entry['Hours']:.2f}")
            with col4:
                if st.button("❌", key=f"del_{date_str}_{i}"):
                    entries_to_remove.append((date_str, i))
            total_hours += entry["Hours"]

# --- Remove entries marked for deletion
for date_str, idx in entries_to_remove:
    if date_str in st.session_state.time_entries and idx < len(st.session_state.time_entries[date_str]):
        del st.session_state.time_entries[date_str][idx]
        if not st.session_state.time_entries[date_str]:
            del st.session_state.time_entries[date_str]
        st.experimental_rerun()

# --- Summary
if total_hours > 0:
    total_pay = total_hours * hourly_rate
    st.markdown("---")
    st.metric("Total Hours Worked", f"{total_hours:.2f} hrs")
    st.metric("Total Pay", f"${total_pay:.2f}")

    if st.button("Clear All Entries"):
        st.session_state.time_entries.clear()
        st.experimental_rerun()
else:
    st.info("Add your first entry to begin calculating.")
