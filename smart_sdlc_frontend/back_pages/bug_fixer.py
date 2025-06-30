# smart_sdlc_frontend/pages/bug_fixer.py

import streamlit as st
import requests
import pyperclip

#st.set_page_config(page_title="🐞 Bug Fixer", layout="wide")

st.title("🐞 Bug Fixer")
st.markdown("Paste in buggy code below. AI will return a clean, corrected version.")

buggy_code = st.text_area("🛠️ Paste Buggy Code", height=300)

if st.button("🚑 Fix Bugs") and buggy_code.strip():
    with st.spinner("Analyzing and fixing bugs..."):
        response = requests.post(
            "http://localhost:8000/ai/fix-bugs",
            json={"buggy_code": buggy_code}
        )

        if response.status_code == 200:
            data = response.json()
            output = data.get("fixed_code", "")
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
                st.success("✅ Fixed Code")
                lang, fixed_code = code_blocks[0]
                st.code(fixed_code, language=lang)
                st.download_button("💾 Download Fixed Code", fixed_code, file_name="fixed_code.py")

                if st.button("📋 Copy to Clipboard"):
                    pyperclip.copy(fixed_code)
                    st.success("Copied!")

                if explanation:
                    with st.expander("🧠 Explanation"):
                        st.markdown(explanation)
        else:
            st.error(f"❌ Error: {response.status_code}")
            st.json(response.json())
