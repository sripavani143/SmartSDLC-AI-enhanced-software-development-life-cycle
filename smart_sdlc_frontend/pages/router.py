import streamlit as st
from pathlib import Path
import importlib.util

# Use session state to track current page
if "page" not in st.session_state:
    st.session_state.page = None

# Choose current page (redirected from main.py)
page_file = st.session_state.page
if not page_file:
    st.error("No page selected. Redirecting to Login.")
    st.switch_page("login")
    st.stop()

# Dynamically load the selected page from pages_back/
page_path = Path(__file__).parent.parent / "pages_back" / f"{page_file}.py"
spec = importlib.util.spec_from_file_location(page_file, page_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
