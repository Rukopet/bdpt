import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

_ = load_dotenv()


def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        _ = st.error("GEMINI_API_KEY not found. Please set it in .env file")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-flash-latest")


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model" not in st.session_state:
        st.session_state.model = init_gemini()


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_bot_response(user_message: str) -> str:
    chat = st.session_state.model.start_chat(history=[])
    
    for msg in st.session_state.messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        chat.history.append({
            "role": role,
            "parts": [msg["content"]]
        })
    
    response = chat.send_message(user_message)
    return response.text


def main():
    st.set_page_config(
        page_title="Gemini Chat Bot",
        page_icon="🤖",
        layout="centered"
    )
    
    st.title("🤖 Gemini Chat Bot")
    
    init_session_state()
    display_chat_history()
    
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_bot_response(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()

