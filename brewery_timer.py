import datetime
import streamlit as st
#page config for industrial HMI feel
st.set_page_config(
    page_title="Brewery Safety Shift Tracker",
    page_icon=":beer:",
    layout="centered",
)
st.title(":beer: Brewery Shift Safety & Productivity Tracker")
st.caption("Personal homelab OT/ICS Operational checklist & shift Timer")

#---------------sesssion state-----------
if "shift_start" not in st.session_state:
    st.session_state.shift_start = None
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "log_entries" not in st.session_state:
    st.session_state.log_entries = []
    #------------sidebar controls-------------
st.sidebar.header("Shift Controls")
shift_duration_minutes = st.sidebar.number_input("Shift Duration (Minutes)", min_value=1, max_value=480, value=30)
col_start, col_reset = st.sidebar.columns(2)
if col_start.button("Start Shift"):
    st.session_state.shift_start = datetime.datetime.now()
    st.session_state.timer_running = True
if col_reset.button("Reset Shift"):
    st.session_state.shift_start = None
    st.session_state.timer_running = False
    st.session_state.log_entries = []
    #section 1: shift stuatus
    
st.subheader("Shift Status") 
if st. session_state.timer_running and st.session_state.shift_start:
    elapsed = datetime.datetime.now() - st.session_state.shift_start
    total_seconds = shift_duration_minutes * 60
    remaining_seconds = max(0, total_seconds - int(elapsed.total_seconds()))

    mins, secs = divmod(remaining_seconds, 60)
    timer_display = f"{mins:02d}:{secs:02d}"
    progress = min(1.0, elapsed.total_seconds() / total_seconds)

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Time Remaining", timer_display)
    metric_col2.metric("Shift Start", st.session_state.shift_start.strftime("%H:%M:%S"))
    metric_col3.metric("Status", "🟢 ACTIVE")

    st.progress(progress)

    if remaining_seconds == 0:
        st.error("🚨 SHIFT COMPLETE: Conduct final OT/ICS safety handoff immediately!")
else:
    st.info("Shift is currently offline. Click **'Start Shift'** in the sidebar to begin tracking.")    
   