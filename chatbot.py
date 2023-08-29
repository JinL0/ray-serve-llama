import requests
import streamlit as st

# App title
st.set_page_config(page_title="🤗💬 HugChat")
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM respons

# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
url = "http://localhost:8000/serve/llama7b"

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            data = {
                "message": prompt
            }
            response = requests.post(url, json=data)
            response = response.json()["result"]
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
