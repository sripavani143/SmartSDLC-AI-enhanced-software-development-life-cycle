import streamlit as st
from pathlib import Path
import importlib.util

st.set_page_config(page_title="SmartSDLC", layout="wide")

# ✅ Initialize session state safely
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "Guest")
st.session_state.setdefault("page", "dashboard")

# ✅ Sidebar layout
with st.sidebar:
    st.title("✨ SmartSDLC")
    st.markdown("### 📌 Features")
    for label, page in [
        ("🏠 Dashboard", "dashboard"),
        ("📂 Upload & Classify", "upload_and_classify"),
        ("💬 Chat Assistant", "chat_assistant"),
        ("🧠 AI Code Generator", "code_generator"),
        ("📄 Code Summarizer", "code_summarizer"),
        ("🐞 Bug Fixer", "bug_fixer"),
        ("🧪 Test Cases Generator", "test_generator"),
        ("📝 Feedback", "feedback")
    ]:
        if st.button(label):
            st.session_state.page = page

    st.markdown("---")
    st.markdown("### 🔒 Authentication")

    if "logged_in" in st.session_state and st.session_state.logged_in:
        st.markdown(f"👤 Logged in as **{st.session_state.username}**")

    for label, page in [
        ("🔐 Login with another account", "login"),
        ("🆕 Add another account", "signup")
    ]:
        if st.button(label):
            st.session_state.page = page

# ✅ Restrict access to features unless logged in
auth_pages = ["login", "signup", "forgot_password", "reset_password"]
if not st.session_state.logged_in and st.session_state.page not in auth_pages:
    st.session_state.page = "login"

# ✅ Map 'main' to 'dashboard' BEFORE assigning current_page
if st.session_state.page == "main":
    st.session_state.page = "dashboard"

# ✅ Dynamically load selected page from pages_back
current_page = st.session_state.get("page", None)
page_path = Path(__file__).parent / "pages_back" / f"{current_page}.py"

if not page_path.exists():
    # ✅ Also try auth_pages folder if not in pages_back
    auth_path = Path(__file__).parent / "auth_pages" / f"{current_page}.py"
    if auth_path.exists():
        page_path = auth_path
    else:
        st.error(f"🚨 Page '{current_page}' not found.")
        st.stop()

# ✅ Load the page
spec = importlib.util.spec_from_file_location(current_page, page_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
