# smart_sdlc_frontend/auth_pages/forgot_password.py

import streamlit as st
import json
from pathlib import Path

USER_DB = Path("smart_sdlc_frontend/utils/users.json")

# Hide sidebar completely
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

st.title("🔁 Reset Your Password")

username_input = st.text_input("Enter your username").strip()
new_password = st.text_input("New Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Reset Password"):
    if not username_input or not new_password or not confirm_password:
        st.error("All fields are required.")
    elif new_password != confirm_password:
        st.error("Passwords do not match.")
    else:
        try:
            users = json.loads(USER_DB.read_text())
            if not isinstance(users, dict):
                st.error("⚠️ User database is corrupted. Expected a dictionary.")
            elif username_input in users:
                users[username_input]["password"] = new_password
                USER_DB.write_text(json.dumps(users, indent=2))
                st.success("✅ Password reset successful! Please login.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("❌ Username not found.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
