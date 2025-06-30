import streamlit as st
import requests

TOGETHER_API_KEY = st.secrets["together_api_key"]
st.set_page_config(page_title = "Simple ChatGPT clone", page_icon = "👽")
st.title("👽 Together.ai Chat Clone")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages: 
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("Ask something")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role" : "user", "content" : user_prompt})

    with st.spinner("Thinking..."):
        payload = {
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
            "messages":st.session_state.messages,
            "temperature": 0.7,
            "top_p" : 0.9
        }

        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        # Make API call
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)

        # Parse and show result
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        else:
            reply = f"❌ Error {response.status_code}: {response.text}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})