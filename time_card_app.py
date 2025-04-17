import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="Time Card Calculator", layout="centered")

st.title("🕒 Time Card Calculator")
st.write("Enter your time entries for each day below. Supports both 24-hour (`14:30`) and 12-hour (`2:30 PM`) formats.")

# --- Initialize session state
if "time_entries" not in st.session_state:
    st.session_state.time_entries = {day: [] for day in [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

# --- Hourly rate
hourly_rate = st.number_input("Hourly pay rate ($):", min_value=0.0, step=0.5, value=20.0)

# --- Time entry form for each day
st.subheader("Enter Time for Each Day")

def parse_time(time_str):
    formats = ["%H:%M", "%I:%M %p"]
    for fmt in formats:
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except ValueError:
            continue
    return None

for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
    with st.expander(f"{day}"):
        col1, col2, col3 = st.columns(3)
        with col1:
            clock_in = st.text_input(f"Clock-in time ({day})", key=f"in_{day}")
        with col2:
            clock_out = st.text_input(f"Clock-out time ({day})", key=f"out_{day}")
        with col3:
            if st.button("Add Entry", key=f"btn_{day}"):
                start = parse_time(clock_in)
                end = parse_time(clock_out)
                if not start or not end:
                    st.error(f"Invalid time format for {day}. Try HH:MM or HH:MM AM/PM.")
                elif end < start:
                    st.error(f"Clock-out time must be after clock-in time for {day}.")
                else:
                    duration = (end - start).total_seconds() / 3600
                    st.session_state.time_entries[day].append({
                        "Clock In": clock_in,
                        "Clock Out": clock_out,
                        "Hours": round(duration, 2)
                    })
                    st.success(f"Entry added for {day}!")

# --- Display entries by day
st.subheader("Time Entries by Day")
total_hours = 0

for day, entries in st.session_state.time_entries.items():
    if entries:
        st.markdown(f"### {day}")
        df = pd.DataFrame(entries)
        st.table(df)
        total_hours += sum(e["Hours"] for e in entries)

# --- Summary
if total_hours > 0:
    total_pay = total_hours * hourly_rate
    st.markdown("---")
    st.metric("Total Hours Worked", f"{total_hours:.2f} hrs")
    st.metric("Total Pay", f"${total_pay:.2f}")

    if st.button("Clear All Entries"):
        st.session_state.time_entries = {day: [] for day in st.session_state.time_entries}
        st.experimental_rerun()
else:
    st.info("Add your first entry to begin calculating.")
