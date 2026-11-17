
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="CommerceCopilot",
    page_icon="🛍️",
    layout="centered"
)

# API address
API_URL = "https://commercecopilot-ra0g.onrender.com/chat"

# Page title
st.title("🛍️ CommerceCopilot")
st.caption("Your AI shopping and customer support assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask CommerceCopilot...")

# Use an example prompt if a visitor clicked one
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

    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("CommerceCopilot is thinking..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_input}
                )

                response.raise_for_status()

                answer = response.json()["response"]

            except requests.exceptions.RequestException as e:
                answer = f"Could not connect to the API: {e}"

            st.markdown(answer)

    # Save assistant response in session
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# Welcome section for first-time visitors
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
            if st.button(example, key=f"example_{i}",
                         use_container_width=True):
                st.session_state.selected_prompt = example
