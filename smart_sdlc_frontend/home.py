import streamlit as st

st.set_page_config(page_title="SmartSDLC", layout="wide")


# 🚨 Block unauthorized access
if not st.session_state.get("logged_in"):
    st.warning("Please log in to continue.")
    st.switch_page("auth_pages/login.py")



st.title("🚀 SmartSDLC Dashboard")
st.markdown("Welcome to your AI-powered command center for accelerating every phase of the Software Development Lifecycle.")

st.markdown("## ✨ Features")

st.page_link("pages/code_generator.py", label=" Go to AI Code Generator", icon="🧠")
st.page_link("pages/bug_fixer.py", label="🐞 Bug Fixer")
st.page_link("pages/test_generator.py", label="🧪 Test Case Generator")
st.page_link("pages/code_summarizer.py", label="📄 Code Summarizer")
st.page_link("pages/upload_and_classify.py", label="📂 Upload & Classify Requirements")
st.page_link("pages/chat_assistant.py", label="💬 Chat Assistant")
st.page_link("pages/feedback.py", label="💬 Submit Feedback")