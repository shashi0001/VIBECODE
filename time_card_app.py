import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Weekly Time Card Calculator", layout="centered")
st.title("📅 Weekly Time Card Calculator")
st.write("Enter your clock-in and clock-out times for each day. Supports both 24-hour (`14:30`) and 12-hour (`2:30 PM`) formats.")

# --- Hourly rate
hourly_rate = st.number_input("Hourly pay rate ($):", min_value=0.0, step=0.5, value=20.0)

# --- Get current week's Sunday
today = date.today()
start_of_week = today - timedelta(days=today.weekday() + 1) if today.weekday() != 6 else today
week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

# --- Time parsing function
def parse_time(time_str):
    formats = ["%H:%M", "%I:%M %p"]
    for fmt in formats:
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except ValueError:
            continue
    return None

# --- Initialize session state
if "weekly_entries" not in st.session_state:
    st.session_state.weekly_entries = {d.isoformat(): {"Clock In": "", "Clock Out": ""} for d in week_dates}

# --- Table UI
st.markdown("### Weekly Time Card")
headers = ["Date", "Day", "In-Time", "Out-Time", "Hours Worked", "Pay"]
data = []

total_hours = 0.0
total_pay = 0.0

for d in week_dates:
    d_str = d.isoformat()
    day_name = d.strftime("%A")
    
    col1, col2 = st.columns(2)
    with col1:
        clock_in = st.text_input(f"{day_name} - In", key=f"{d_str}_in", value=st.session_state.weekly_entries[d_str]["Clock In"])
    with col2:
        clock_out = st.text_input(f"{day_name} - Out", key=f"{d_str}_out", value=st.session_state.weekly_entries[d_str]["Clock Out"])

    st.session_state.weekly_entries[d_str]["Clock In"] = clock_in
    st.session_state.weekly_entries[d_str]["Clock Out"] = clock_out

    start = parse_time(clock_in) if clock_in else None
    end = parse_time(clock_out) if clock_out else None

    if start and end and end > start:
        duration = (end - start).total_seconds() / 3600
        pay = duration * hourly_rate
        total_hours += duration
        total_pay += pay
    else:
        duration = 0.0
        pay = 0.0

    data.append([
        d.strftime("%Y-%m-%d"),
        day_name,
        clock_in,
        clock_out,
        round(duration, 2),
        f"${round(pay, 2):.2f}"
    ])

# --- Add totals row
data.append(["", "Total", "", "", round(total_hours, 2), f"${round(total_pay, 2):.2f}"])

# --- Display table (without row numbers)
df = pd.DataFrame(data, columns=headers)
st.dataframe(df.style.hide(axis="index"))

# --- Export functions
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Weekly Time Card")
    return output.getvalue()

# --- Download buttons
st.markdown("### 📤 Export Report")
col1, col2 = st.columns(2)
with col1:
    st.download_button("Download as CSV", data=convert_df_to_csv(df), file_name="weekly_time_card.csv", mime="text/csv")
with col2:
    st.download_button("Download as Excel", data=convert_df_to_excel(df), file_name="weekly_time_card.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
