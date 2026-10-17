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
    