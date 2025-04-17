import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Time Card Calculator", layout="centered")

st.title("🕒 Time Card Calculator")
st.write("Enter your time entries below. Supports both 24-hour (`14:30`) and 12-hour (`2:30 PM`) formats.")

# --- Initialize session state
if "time_entries" not in st.session_state:
    st.session_state.time_entries = []

# --- Hourly rate
hourly_rate = st.number_input("Hourly pay rate ($):", min_value=0.0, step=0.5, value=20.0)

# --- Time entry form
with st.form("time_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        day = st.selectbox("Day of the Week", [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ])
    with col2:
        clock_in = st.text_input("Clock-in time", placeholder="e.g., 8:00 AM or 08:00")
    with col3:
        clock_out = st.text_input("Clock-out time", placeholder="e.g., 5:00 PM or 17:00")

    submitted = st.form_submit_button("Add Entry")

    def parse_time(time_str):
        formats = ["%H:%M", "%I:%M %p"]
        for fmt in formats:
            try:
                return datetime.strptime(time_str.strip(), fmt)
            except ValueError:
                continue
        return None

    if submitted:
        start = parse_time(clock_in)
        end = parse_time(clock_out)

        if not start or not end:
            st.error("Invalid time format. Try HH:MM or HH:MM AM/PM.")
        elif end < start:
            st.error("Clock-out time must be after clock-in time.")
        else:
            duration = (end - start).total_seconds() / 3600
            st.session_state.time_entries.append({
                "Day": day,
                "Clock In": clock_in,
                "Clock Out": clock_out,
                "Hours": round(duration, 2)
            })
            st.success("Entry added!")

# --- Display entries
if st.session_state.time_entries:
    st.subheader("Time Entries")
    st.table(st.session_state.time_entries)

    total_hours = sum(entry["Hours"] for entry in st.session_state.time_entries)
    total_pay = total_hours * hourly_rate

    st.markdown("---")
    st.metric("Total Hours Worked", f"{total_hours:.2f} hrs")
    st.metric("Total Pay", f"${total_pay:.2f}")

    # Option to clear entries
    if st.button("Clear All Entries"):
        st.session_state.time_entries.clear()
        st.experimental_rerun()
else:
    st.info("Add your first entry above to begin calculating.")
