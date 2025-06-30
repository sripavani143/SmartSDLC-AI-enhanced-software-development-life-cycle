import streamlit as st
import requests

st.title("📄 Upload and Classify PDF")
st.markdown("Upload a PDF and classify its content into SDLC phases using AI.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file and st.button("🔍 Classify SDLC Phases"):
    with st.spinner("Analyzing PDF..."):
        try:
            response = requests.post(
                "http://localhost:8000/ai/upload-pdf",
                files={"file": uploaded_file.getvalue()},
            )
            if response.status_code == 200:
                result = response.json()

                if "result" in result and isinstance(result["result"], str):
                    st.markdown(f"```text\n{result['result']}\n```")

                else:
                    st.warning("No results returned or unexpected format.")
            else:
                st.error(f"❌ Something went wrong. Status code: {response.status_code}")
                try:
                    st.json(response.json())
                except Exception:
                    st.text(response.text)
        except Exception as e:
            st.error(f"❌ Failed to send request: {e}")
