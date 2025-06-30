# smart_sdlc_frontend/auth_pages/reset_password.py

import streamlit as st
import json
from pathlib import Path

USER_DB = Path("smart_sdlc_frontend/utils/users.json")

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔁 Reset Password")

otp_input = st.text_input("Enter OTP sent to your email")
new_password = st.text_input("New Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Reset Password"):
    if "otp" not in st.session_state or "reset_email" not in st.session_state:
        st.error("Session expired. Please restart the forgot password process.")
    elif otp_input != st.session_state.otp:
        st.error("Incorrect OTP.")
    elif new_password != confirm_password:
        st.error("Passwords do not match.")
    else:
        users = json.loads(USER_DB.read_text())
        for u in users:
            if u["email"] == st.session_state.reset_email:
                u["password"] = new_password
                break
        USER_DB.write_text(json.dumps(users, indent=2))
        st.success("✅ Password reset successful! Please login.")
        st.session_state.step = 1
        st.switch_page("login.py")
