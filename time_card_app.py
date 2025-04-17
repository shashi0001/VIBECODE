import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import calendar

st.set_page_config(page_title="Time Card Calculator", layout="centered")

st.title("🕒 Time Card Calculator")
st.write("Select a date and enter your time entries. Supports both 24-hour (`14:30`) and 12-hour (`2:30 PM`) formats.")

# --- Initialize session state
if "time_entries" not in st.session_state:
    st.session_state.time_entries = {}

# --- Hourly rate
hourly_rate = st.number_input("Hourly pay rate ($):", min_value=0.0, step=0.5, value=20.0)

# --- Date selector
selected_date = st.date_input("Select a date")
day_of_week = selected_date.strftime("%A")

# --- Input for time
st.subheader(f"Enter Time for {day_of_week}, {selected_date.strftime('%B %d, %Y')}")

col1, col2, col3 = st.columns(3)
with col1:
    clock_in = st.text_input("Clock-in time", placeholder="e.g., 08:00 or 8:00 AM", key="in_time")
with col2:
    clock_out = st.text_input("Clock-out time", placeholder="e.g., 17:00 or 5:00 PM", key="out_time")
with col3:
    def parse_time(time_str):
        formats = ["%H:%M", "%I:%M %p"]
        for fmt in formats:
            try:
                return datetime.strptime(time_str.strip(), fmt)
            except ValueError:
                continue
        return None

    if st.button("Add Entry"):
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

# --- Display entries by date
st.subheader("Time Entries")
total_hours = 0

all_entries = []
for date_str, entries in sorted(st.session_state.time_entries.items()):
    all_entries.extend(entries)
    total_hours += sum(e["Hours"] for e in entries)

if all_entries:
    df = pd.DataFrame(all_entries)
    st.table(df)

    total_pay = total_hours * hourly_rate
    st.markdown("---")
    st.metric("Total Hours Worked", f"{total_hours:.2f} hrs")
    st.metric("Total Pay", f"${total_pay:.2f}")

    if st.button("Clear All Entries"):
        st.session_state.time_entries.clear()
        st.experimental_rerun()
else:
    st.info("Add your first entry to begin calculating.")
