import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

_ = load_dotenv()

AVAILABLE_MODELS = {
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.5 Pro": "gemini-2.5-pro",
}


def init_gemini(model_name: str, system_prompt: str | None = None):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        _ = st.error("GEMINI_API_KEY not found. Please set it in .env file")
        st.stop()
    
    genai.configure(api_key=api_key)
    
    if system_prompt:
        return genai.GenerativeModel(
            model_name,
            system_instruction=system_prompt
        )
    return genai.GenerativeModel(model_name)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = ""
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "Gemini 2.5 Flash"
    if "model" not in st.session_state:
        model_id = AVAILABLE_MODELS[st.session_state.selected_model]
        st.session_state.model = init_gemini(model_id, st.session_state.system_prompt)


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            _ = st.markdown(message["content"])


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
    
    _ = st.title("🤖 Gemini Chat Bot")
    
    init_session_state()
    
    _ = st.caption(f"Current model: **{st.session_state.selected_model}**")
    
    with st.sidebar:
        _ = st.header("Settings")
        
        selected_model_name = st.selectbox(
            "Model",
            options=list(AVAILABLE_MODELS.keys()),
            index=list(AVAILABLE_MODELS.keys()).index(st.session_state.selected_model),
            help="Choose the Gemini model to use"
        )
        
        if selected_model_name != st.session_state.selected_model:
            st.session_state.selected_model = selected_model_name
            model_id = AVAILABLE_MODELS[selected_model_name]
            st.session_state.model = init_gemini(model_id, st.session_state.system_prompt)
            _ = st.success(f"Switched to {selected_model_name}")
        
        new_system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=150,
            help="Define the bot's behavior and personality"
        )
        
        if new_system_prompt != st.session_state.system_prompt:
            st.session_state.system_prompt = new_system_prompt
            model_id = AVAILABLE_MODELS[st.session_state.selected_model]
            st.session_state.model = init_gemini(model_id, new_system_prompt)
            _ = st.success("System prompt updated!")
        
        _ = st.divider()
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    display_chat_history()
    
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            _ = st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_bot_response(prompt)
                _ = st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

