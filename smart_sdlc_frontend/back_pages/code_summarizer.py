# smart_sdlc_frontend/pages/code_summarizer.py

import streamlit as st
import requests
import pyperclip

#st.set_page_config(page_title="📄 Code Summarizer", layout="wide")

st.title("📄 Code Summarizer")
st.markdown("Paste any code snippet below. AI will summarize its logic for you.")

code_input = st.text_area("🧾 Enter Code", height=300)

if st.button("📄 Summarize Code") and code_input.strip():
    with st.spinner("Summarizing code..."):
        response = requests.post(
            "http://localhost:8000/ai/summarize-code",
            json={"code": code_input}
        )

        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", "")

            if summary:
                st.success("✅ Summary")
                with st.expander("📘 Explanation", expanded=True):
                    st.markdown(summary)
                if st.button("📋 Copy Summary"):
                    pyperclip.copy(summary)
                    st.success("Copied to clipboard!")
            else:
                st.warning("AI returned an empty summary.")
        else:
            st.error(f"❌ Error: {response.status_code}")
            st.json(response.json())
