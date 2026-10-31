import streamlit as st
import datetime
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Brewery Safety & OT Incident Simulator",
    page_icon="🍺",
    layout="wide"
)

# --- Initialize Persistent Session State ---
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "shift_start" not in st.session_state:
    st.session_state.shift_start = None
if "last_action_time" not in st.session_state:
    st.session_state.last_action_time = None
if "log_entries" not in st.session_state:
    st.session_state.log_entries = []
if "tank_ruptured" not in st.session_state:
    st.session_state.tank_ruptured = False

# Helper function to record events to the audit trail
def log_event(event_text):
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.log_entries.append(f"[{now_str}] {event_text}")
    st.session_state.last_action_time = datetime.datetime.now()

# --- Sidebar: Shift & Operator Controls ---
st.sidebar.header("Shift Controls")
operator_name = st.sidebar.text_input("Operator Name", value="Lead Cellar Tech")
shift_duration_minutes = st.sidebar.number_input(
    "Shift Duration (Minutes)", min_value=1, max_value=480, value=30
)

col_s1, col_s2 = st.sidebar.columns(2)
if col_s1.button("Start Shift", use_container_width=True):
    st.session_state.timer_running = True
    st.session_state.shift_start = datetime.datetime.now()
    st.session_state.last_action_time = datetime.datetime.now()
    st.session_state.tank_ruptured = False
    log_event(f"Shift initiated by {operator_name} (Duration: {shift_duration_minutes} min)")
    st.rerun()

if col_s2.button("Reset Shift", use_container_width=True):
    st.session_state.timer_running = False
    st.session_state.shift_start = None
    st.session_state.last_action_time = None
    st.session_state.tank_ruptured = False
    log_event(f"Shift reset by {operator_name}")
    st.rerun()

# --- Main Dashboard Header ---
st.title("🍺 Brewery Shift Safety & OT Incident Simulator")
st.caption(f"Operator on Duty: **{operator_name}** | Homelab OT/ICS Simulation Environment")

# --- Section 1: Dynamic Shift Status & Inactivity Monitor ---
st.subheader("Shift Status")

if st.session_state.timer_running and st.session_state.shift_start:
    now = datetime.datetime.now()
    elapsed = now - st.session_state.shift_start
    total_seconds = shift_duration_minutes * 60
    remaining_seconds = max(0, total_seconds - int(elapsed.total_seconds()))

    mins, secs = divmod(remaining_seconds, 60)
    timer_display = f"{mins:02d}:{secs:02d}"
    progress = min(1.0, elapsed.total_seconds() / total_seconds)

    # Calculate inactive time since last checkpoint action
    seconds_since_action = (now - st.session_state.last_action_time).total_seconds()
    
    if seconds_since_action > 60:
        status_label = "⚠️ IDLE / UNATTENDED"
    else:
        status_label = "🟢 ACTIVE MONITORING"

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Time Remaining", timer_display)
    metric_col2.metric("Shift Start", st.session_state.shift_start.strftime("%H:%M:%S"))
    metric_col3.metric("System State", status_label)

    st.progress(progress)

    if remaining_seconds == 0:
        st.error("🚨 SHIFT DURATION EXPIRED: Complete all final safety handoffs!")
else:
    st.info("Shift is currently offline. Click **'Start Shift'** in the sidebar to begin tracking.")

# --- Section 2: Interactive Safety Checkpoints with Auto-Logging ---
st.divider()
st.subheader("📋 OT/ICS Operational Safety Checkpoints")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### Critical Hardware & Environment")
    check_temp = st.checkbox(
        "Verify Glycol / Cold Room Chiller Setpoints (≤ 4°C)",
        key="chk_temp",
        on_change=lambda: log_event(f"Chiller setpoints verified (≤ 4°C) by {operator_name}")
    )
    check_valves = st.checkbox(
        "Confirm Manual & Solenoid Pressure Relief Valves Clear",
        key="chk_valves",
        on_change=lambda: log_event(f"Pressure relief valves inspected clear by {operator_name}")
    )
    check_co2 = st.checkbox(
        "Inspect Ambient CO2 Monitor & Ventilation Fans",
        key="chk_co2",
        on_change=lambda: log_event(f"CO2 monitor & exhaust ventilation verified by {operator_name}")
    )

with col_b:
    st.markdown("### Cyber-Physical & Network Integrity")
    check_plc = st.checkbox(
        "Inspect PLC/HMI Enclosures (No unauthorized USB/cables)",
        key="chk_plc",
        on_change=lambda: log_event(f"Physical PLC enclosure integrity checked by {operator_name}")
    )
    check_telemetry = st.checkbox(
        "Telemetry Sanity Check (Sensor values within nominal ranges)",
        key="chk_telemetry",
        on_change=lambda: log_event(f"Sensor telemetry sanity cross-check passed by {operator_name}")
    )
    check_remote = st.checkbox(
        "Verify External Remote Maintenance Sessions Logged / Closed",
        key="chk_remote",
        on_change=lambda: log_event(f"Remote vendor maintenance connections closed by {operator_name}")
    )

total_checks = sum([check_temp, check_valves, check_co2, check_plc, check_telemetry, check_remote])
st.progress(total_checks / 6)
st.caption(f"Completed {total_checks}/6 Operational Safeguards")

# --- Section 3: Simulated Tank Overheat & Explosion Hazard ---
st.divider()
st.subheader("🔥 Fermentation Tank 01 — Thermal & Pressure Simulation")
st.write("Simulate physical reaction to runaway heating (e.g., thermostat hack or cooling solenoid failure):")

tank_col1, tank_col2 = st.columns([2, 1])

with tank_col1:
    # Temperature Slider
    sim_temp = st.slider("Simulated Tank Temperature (°C)", min_value=0, max_value=60, value=4, step=1)
    
    # Calculate simulated pressure based on temperature (Gay-Lussac's Law principle)
    # Baseline nominal pressure ~12 PSI at 4°C, climbing dramatically with heat
    sim_pressure = round(12 + ((sim_temp - 4) * 0.95), 1)

with tank_col2:
    st.metric("Internal Temperature", f"{sim_temp} °C", delta=f"{sim_temp - 4} °C from baseline", delta_color="inverse")
    st.metric("Internal Vessel Pressure", f"{sim_pressure} PSI", delta=f"{round(sim_pressure - 12, 1)} PSI", delta_color="inverse")

# Simulation Warning / Explosion Logic
if sim_temp > 40:
    if not check_valves:
        st.session_state.tank_ruptured = True
        st.error("""
        💥 **CATASTROPHIC FAILURE: TANK EXPLOSION / RUPTURE DETECTED!**
        
        * **Cause:** Runaway thermal expansion drove internal pressure past the vessel's burst rating (> 45 PSI).
        * **Root OT Vulnerability:** Manual pressure relief valves were NOT verified or cleared before heating.
        * **Safety Incident:** Structural tank rupture, hot liquid scald hazard, and sudden CO2 blowout.
        """)
        log_event(f"🚨 CRITICAL ALARM: Tank 01 RUPTURED at {sim_temp}°C / {sim_pressure} PSI (Valves blocked)!")
    else:
        st.warning("""
        ⚠️ **HIGH TEMPERATURE WARNING — RELIEF VALVES ENGAGED**
        
        Thermal expansion exceeded 40°C, but mechanical pressure relief valves opened successfully to vent gas.
        Batch spoiled, but catastrophic tank rupture was averted by physical safeguards.
        """)
        log_event(f"⚠️ WARNING: Tank 01 thermal overload ({sim_temp}°C) — Mechanical relief vented successfully.")

elif sim_temp > 15:
    st.warning("⚠️ Elevated Fermentation Temperature: Off-flavors developing. Glycol chilling system failing to keep setpoint.")

# --- Section 4: Shift Log & Audit Trail ---
st.divider()
st.subheader("📜 Operational Audit Log")

if st.session_state.log_entries:
    for entry in reversed(st.session_state.log_entries):
        st.markdown(f"`{entry}`")
else:
    st.caption("No operational events logged for this session yet.")