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
    ### #section 2: OT/ICS operationsl safety cheklists
    st.divider()
st.subheader("OT/ICS Operational Safety Checklist")

col_a, col_b = st.columns(2)
with col_a:   
    st.markdown("### Critical hardware & Environment")
    check_temp = st.checkbox("Verify Glycol / Cold Room Chiller Setpoints (≤ 4°C)")
    check_valves = st.checkbox("Confirm Manual & Solenoid Pressure Relief Valves Clear")
    check_co2 = st.checkbox("Inspect Ambient CO2 Monitor & Ventilation Fans")
    
with col_b:
    st.markdown("### Cyber-Physical & Network Integrity")
    check_plc = st.checkbox("Inspect PLC/HMI Enclosures (No unauthorized USB/cables)")
    check_telemetry = st.checkbox("Telemetry Sanity Check (Sensor values within nominal ranges)")
    check_remote = st.checkbox("Verify External Remote Maintenance Sessions Logged / Closed")   
   
   # Calculate total checks completed
total_checks = sum([check_temp, check_valves, check_co2, check_plc, check_telemetry, check_remote])
if total_checks == 6:
    st.success("✅ All physical and cyber safety checkpoints verified!")
   
   
    # --- Section 3: Shift Log & Audit Trail ---
st.divider()
st.subheader("📜 Operational Audit Log")

if st.session_state.log_entries:
    for entry in reversed(st.session_state.log_entries):
        st.write(f"- {entry}")
else:
    st.caption("No operational events logged for this session yet.")