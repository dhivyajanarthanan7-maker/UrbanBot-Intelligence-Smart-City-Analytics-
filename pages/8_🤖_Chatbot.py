import streamlit as st
from chatbot.chatbot_logic import chatbot_response

st.set_page_config(page_title="UrbanBot AI Assistant", layout="centered")

st.title("🤖 UrbanBot – Smart City AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about traffic, air quality, accidents, crowd, complaints...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response = chatbot_response(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
