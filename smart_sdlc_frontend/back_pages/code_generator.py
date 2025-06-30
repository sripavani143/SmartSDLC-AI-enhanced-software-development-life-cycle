import streamlit as st
import requests
import pyperclip
from utils.history import save_history, load_history, clear_history
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.title("🧠 AI Code Generator")
st.markdown("Enter a task or requirement and let the AI generate code for you!")

# Sidebar
with st.sidebar:
    st.title("🕘 History")
    history = load_history()
    for entry in reversed(history):
        st.markdown(f"🔹 {entry['task']}")
    if st.button("🆕 New Chat"):
        st.session_state['task_input'] = ""
        st.rerun()
    if st.button("🗑️ Clear History"):
        clear_history()
        st.rerun()

# Input area
if 'task_input' not in st.session_state:
    st.session_state['task_input'] = ""

task = st.text_input("📝 Enter your task", value=st.session_state['task_input'])
st.session_state['task_input'] = task

if task:
    st.markdown("✏️ You can edit your task anytime above.")

if st.button("🚀 Generate Code") and task:
    with st.spinner("Generating code..."):
        response = requests.post("http://localhost:8000/ai/generate-code", json={"task": task})
        if response.status_code == 200:
            data = response.json()
            generated_code = data.get("code", "").strip()

            # Extract only clean code
            code = ""
            if "```" in generated_code:
                parts = generated_code.split("```")
                for part in parts:
                    part = part.strip()
                    if part.lower().startswith(("python", "java", "c", "cpp", "c++", "javascript")):
                        lang, *lines = part.split("\n")
                        code = "\n".join(lines).strip()
                        detected_lang = lang.strip().lower()
                    elif not code:
                        code = part.strip()
            else:
                code = generated_code.strip()

            # Try to infer language for highlighting and file extension
            if "java" in task.lower():
                detected_lang = "java"
                file_name = "generated_code.java"
            elif "c++" in task.lower() or "cpp" in task.lower():
                detected_lang = "cpp"
                file_name = "generated_code.cpp"
            elif "c program" in task.lower() or task.lower().startswith("write a c "):
                detected_lang = "c"
                file_name = "generated_code.c"
            elif "c#" in task.lower():
                detected_lang = "csharp"
                file_name = "generated_code.cs"
            elif "javascript" in task.lower():
                detected_lang = "javascript"
                file_name = "generated_code.js"
            elif "html" in task.lower():
                detected_lang = "html"
                file_name = "generated_code.html"
            elif "sql" in task.lower():
                detected_lang = "sql"
                file_name = "generated_code.sql"
            else:
                detected_lang = "python"
                file_name = "generated_code.py"

            st.success("✅ Generated Code")
            st.code(code, language=detected_lang)
            st.download_button("💾 Download Code", code, file_name=file_name)

            if st.button("📋 Copy to Clipboard", key=f"copy_{task}"):
                pyperclip.copy(code)
                st.success("Copied to clipboard!")

            save_history({
                "task": task,
                "code": code,
                "explanation": ""  # Keep empty for consistency
            })

        else:
            st.error(f"❌ Unexpected response: {response.status_code}")
