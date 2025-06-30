# smart_sdlc_frontend/pages/test_generator.py

import streamlit as st
import requests
import pyperclip

#st.set_page_config(page_title="🧪 Test Case Generator", layout="wide")

st.title("🧪 Test Case Generator")
st.markdown("Enter a code snippet or requirement, and generate unit test cases using AI.")

input_text = st.text_area("🧾 Enter Code or Requirement", height=300)

if st.button("🧪 Generate Test Cases") and input_text.strip():
    with st.spinner("Generating test cases..."):
        response = requests.post(
            "http://localhost:8000/ai/generate-tests",
            json={"input_text": input_text}
        )

        if response.status_code == 200:
            data = response.json()
            output = data.get("test_code", "")
            code_blocks = []
            explanation = ""

            if "```" in output:
                parts = output.split("```")
                for part in parts:
                    part = part.strip()
                    if part.startswith("python") or part.startswith("c") or part.startswith("cpp"):
                        lang, *lines = part.split("\n")
                        code = "\n".join(lines).strip()
                        code_blocks.append((lang.strip(), code))
                    elif part:
                        explanation = part.strip()
            else:
                code_blocks = [("python", output)]

            if code_blocks:
                st.success("✅ Generated Test Cases")
                lang, test_code = code_blocks[0]
                st.code(test_code, language=lang)
                st.download_button("💾 Download Tests", test_code, file_name="test_cases.py")

                if st.button("📋 Copy to Clipboard"):
                    pyperclip.copy(test_code)
                    st.success("Copied!")

                if explanation:
                    with st.expander("🧠 Explanation"):
                        st.markdown(explanation)
        else:
            st.error(f"❌ Error: {response.status_code}")
            st.json(response.json())
