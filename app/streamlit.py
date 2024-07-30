import streamlit as st
import requests
import uuid

st.title("Chat with Lucky!")

# Generate a unique session ID if not already present
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_response(query):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"query": query, "session_id": session_id},
            timeout=30  # Increase the timeout to 30 seconds
        )
        response.raise_for_status()  # Raise an error for bad status codes
        response_json = response.json()
        if "response" in response_json:
            return response_json["response"]
        else:
            return "Error: No response found in server reply."
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return "Error: Request failed."
    except ValueError:
        st.error("Error: Unable to decode JSON response from server.")
        return "Error: Unable to decode JSON response from server."

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Hi, how can I assist you today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = get_response(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})