# smart_sdlc_frontend/pages/chat_assistant.py

import streamlit as st
import requests
import pyperclip

#st.set_page_config(page_title="💬 Chat Assistant", layout="wide")

st.title("💬 Chat Assistant")
st.markdown("Ask the AI assistant anything about coding, debugging, architecture, tools, etc.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("🧠 Your Message")

if st.button("📨 Send") and user_input.strip():
    st.session_state.chat_history.append(("You", user_input))

    with st.spinner("AI is thinking..."):
        response = requests.post(
            "http://localhost:8000/ai/chat",
            json={"message": user_input}
        )

        if response.status_code == 200:
            reply = response.json().get("reply", "")
            st.session_state.chat_history.append(("AI", reply))
        else:
            st.session_state.chat_history.append(("AI", f"❌ Error: {response.status_code}"))

# Display history from top to bottom, without repeating input at the bottom
for sender, message in st.session_state.chat_history:
    if sender == "You":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("assistant"):
            st.markdown(message)
