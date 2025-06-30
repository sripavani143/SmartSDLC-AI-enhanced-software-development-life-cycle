import streamlit as st
import json
from pathlib import Path

USER_DB = Path("smart_sdlc_frontend/utils/users.json")

# Hide sidebar and center content
st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none !important;
    }
    .block-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        padding-top: 1 !important;
    }
    div[data-baseweb="input"] {
        max-width: 400px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Login to SmartSDLC")

username = st.text_input("Username").strip()
password = st.text_input("Password", type="password").strip()

# Load users
users = {}
if USER_DB.exists():
    try:
        users = json.loads(USER_DB.read_text())
    except:
        st.error("⚠️ Failed to load user database.")

if st.button("Sign In"):
    if not username or not password:
        st.error("Please enter both username and password.")
    else:
        user = users.get(username)
        if user and user.get("password") == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "dashboard"
            st.success("✅ Login successful! Redirecting to Dashboard...")
            st.rerun()
        else:
            st.error("❌ Invalid credentials.")

if st.button("Forgot Password?"):
    st.session_state.page = "forgot_password"
    st.rerun()

st.markdown("---")
st.markdown("Don't have an account?")
if st.button("Create Account"):
    st.session_state.page = "signup"
    st.rerun()
