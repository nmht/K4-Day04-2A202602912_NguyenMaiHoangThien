import streamlit as st
from pathlib import Path
import sys

# Ensure starter_v0 is in sys.path
sys.path.append(str(Path(__file__).parent))

from chat import run_model_tool_loop, trim_history
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools

st.set_page_config(page_title="IT Helpdesk Agent", page_icon="🤖")

st.title("IT Helpdesk Agent (Phase 6)")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = Path("artifacts/system_prompt.md").read_text(encoding="utf-8")

if "tools" not in st.session_state:
    tool_declarations = load_tool_declarations(Path("artifacts/tools.yaml"))
    st.session_state.tools = to_openai_tools(tool_declarations)

if "provider" not in st.session_state:
    st.session_state.provider = make_provider("gemini")

# Display chat messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Nhập yêu cầu của bạn..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.history.append({"role": "user", "content": prompt})

    messages = [
        {"role": "system", "content": st.session_state.system_prompt},
        *trim_history(st.session_state.history[:-1], 5),
        {"role": "user", "content": prompt}
    ]

    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                result = run_model_tool_loop(
                    provider=st.session_state.provider,
                    messages=messages,
                    tools=st.session_state.tools,
                    model="gemini-3.1-flash-lite",
                    max_tool_rounds=4
                )
                assistant_text = result.get("assistant_text", "")
                st.markdown(assistant_text)
                
                # Show tool events if any
                if result.get("tool_events"):
                    with st.expander("🛠️ Tool Executions"):
                        for event in result["tool_events"]:
                            st.json(event)
                
                st.session_state.history.append({"role": "assistant", "content": assistant_text})
            except Exception as e:
                st.error(f"Error: {str(e)}")
