import streamlit as st
import json
import re
from pathlib import Path

USER_DB = Path("smart_sdlc_frontend/utils/users.json")

# Hide sidebar and center layout
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

# Validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Save user to JSON DB
def save_user(username, email, password):
    users = {}
    if USER_DB.exists():
        try:
            users = json.loads(USER_DB.read_text())
        except:
            users = {}
    users[username] = {"email": email, "password": password}
    USER_DB.write_text(json.dumps(users, indent=2))

# ⛏ Reset account_created if user navigated here
if "page" in st.session_state and st.session_state.page != "signup":
    st.session_state.account_created = False
    st.session_state.page = "signup"

# Initialize state
if "account_created" not in st.session_state:
    st.session_state.account_created = False

st.title("📝 Create New Account")

if not st.session_state.account_created:
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not username or not email or not password:
            st.error("All fields are required.")
        elif not is_valid_email(email):
            st.error("❌ Invalid email format.")
        elif password != confirm_password:
            st.error("❌ Passwords do not match.")
        else:
            save_user(username, email, password)
            st.session_state.account_created = True

    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Login"):
        st.session_state.page = "login"
        st.rerun()
else:
    st.success("✅ Account created! You can now login.")
    if st.button("➡️ Go to Login"):
        st.session_state.page = "login"
        st.session_state.account_created = False  # ✅ reset it here too
        st.rerun()


