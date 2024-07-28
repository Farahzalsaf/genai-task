import streamlit as st
import requests
import uuid

st.title("Chat with Lucky")

# Generate a unique session ID if not already present
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

def get_response(query, session_id):
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"query": query, "session_id": session_id}
    )
    return response.json()["response"]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = get_response(prompt, session_id)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
