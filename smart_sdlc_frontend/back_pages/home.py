# smart_sdlc_frontend/pages/home.py

import streamlit as st

# ✅ Access control
if not st.session_state.get("logged_in"):
    st.warning("🔒 Please login first.")
    st.switch_page("pages_back/login.py")

st.set_page_config(page_title="Home - SmartSDLC", layout="wide")
st.sidebar.title("Welcome")

st.sidebar.markdown(f"👤 Logged in as **{st.session_state['username']}**")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("main.py")

st.title("🏠 SmartSDLC Dashboard")
st.markdown("Welcome to your AI-powered SDLC workspace!")
