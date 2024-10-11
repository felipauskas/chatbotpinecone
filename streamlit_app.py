import streamlit as st
import requests
import json

# Show title and description.
st.title("💬 Pinecone Chat Assistant")
st.write(
    "This is a simple chatbot that uses Pinecone's Chat Assistant to generate responses. "
    "You can learn more about Pinecone's Assistant in their [documentation](https://docs.pinecone.io/docs/assistant)."
)

# Accessing API keys from secrets
pinecone_api_key = st.secrets["api_keys"]["pinecone_api_key"]
pinecone_environment = st.secrets["api_keys"]["pinecone_environment"]
openai_api_key = st.secrets["api_keys"]["openai_api_key"]
claude_api_key = st.secrets["api_keys"]["claude_api_key"]

# Ask user for their Assistant name via `st.text_input`.
assistant_name = st.text_input("Assistant Name")
if not assistant_name:
    st.info("Please add your Assistant name to continue.", icon="🗝️")
else:
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field
    if prompt := st.chat_input("Type your message"):
        # Store and display the user's message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare the payload for Pinecone API
        url = f"https://prod-1-data.ke.pinecone.io/assistant/chat/{assistant_name}"
        headers = {
            "Api-Key": pinecone_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "messages": st.session_state.messages,
            "stream": False,
            "model": "gpt-4o"  # You can change the model if needed
        }

        # Make a POST request to Pinecone API
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            result = response.json()
            assistant_message = result.get("message", {}).get("content", "")
            # Display assistant's response
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
            # Store assistant's response
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        else:
            st.error(f"Error: {response.status_code} - {response.text}")