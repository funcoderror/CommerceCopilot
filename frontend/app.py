
import sys
import uuid
from pathlib import Path

import streamlit as st

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Page configuration
st.set_page_config(
    page_title="CommerceCopilot",
    page_icon="🛍️",
    layout="centered"
)

# Initialize session data
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Page title
st.title("🛍️ CommerceCopilot")
st.caption("Your AI shopping and customer support assistant")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask CommerceCopilot...")

# Handle example prompts
if st.session_state.get("selected_prompt"):
    user_input = st.session_state.pop("selected_prompt")

if user_input:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("CommerceCopilot is thinking..."):

            try:
                from src.tools.tool_calling import run_tool_assistant

                answer = run_tool_assistant(
                    user_input,
                    session_id=st.session_state.session_id
                )

            except Exception as e:
                answer = f"Something went wrong: {str(e)}"

            st.markdown(answer)

    # Save assistant response in Streamlit session
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# Welcome section
if not st.session_state.messages:

    st.markdown("## Welcome to CommerceCopilot! 👋")
    st.markdown(
        "Your AI-powered e-commerce shopping and customer "
        "support assistant. Ask questions about products, "
        "policies, and product compatibility."
    )

    st.markdown("### 💡 Try asking")

    examples = [
        "Find me products under ₹2,000",
        "What is your return and refund policy?",
        "Tell me more about a particular product",
        "Which phone case is compatible with my phone?"
    ]

    cols = st.columns(2)

    for i, example in enumerate(examples):
        with cols[i % 2]:
            if st.button(
                example,
                key=f"example_{i}",
                use_container_width=True
            ):
                st.session_state.selected_prompt = example
                st.rerun()
