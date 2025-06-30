# smart_sdlc_frontend/pages/feedback.py

import streamlit as st
import requests

#st.set_page_config(page_title="💬 Submit Feedback", layout="wide")

st.title("💬 Submit Feedback")
st.markdown("Have suggestions or issues? Let us know!")

feedback_input = st.text_area("✍️ Your Feedback", height=200)

if st.button("📬 Send Feedback") and feedback_input.strip():
    with st.spinner("Sending feedback..."):
        response = requests.post(
            "http://localhost:8000/ai/submit-feedback",
            json={"feedback": feedback_input}
        )
        if response.status_code == 200:
            msg = response.json().get("message", "")
            st.success(msg)
            st.empty()  # reset input
        else:
            err = response.json().get("detail", "Unknown error")
            st.error(f"❌ Could not send feedback: {err}")
