
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="CommerceCopilot",
    page_icon="🛍️",
    layout="centered"
)

# API address
API_URL = "http://127.0.0.1:8000/chat"

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
user_input = st.chat_input("Ask me anything about products, orders or policies...")

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
