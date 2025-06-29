import streamlit as st
from chatbot.chat_session import ChatSession
import requests
import re

API_URL_CREATE = "http://127.0.0.1:8000/complaints"
API_URL_TRACK = "http://127.0.0.1:8000/complaints/{}"

# Dummy knowledge base for demo
KB = {
    "delayed delivery": "If your delivery is delayed, you can file a complaint and our team will assist you.",
    "refund": "Refunds are processed within 5-7 business days after approval."
}

def retrieve_from_kb(query):
    for k, v in KB.items():
        if k in query.lower():
            return v
    return "I'm here to help with your complaints or questions!"

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)

# Initialize session state only once
if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("\U0001F4E2 Grievance RAG Chatbot")

def clear_input():
    st.session_state.inp = ""

# Only one text_input with key='inp' in the entire script
user_input = st.text_input("Type your message below:", key="inp")

if st.button("Send"):
    if user_input:
        response = st.session_state.chat_session.process(user_input)
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Bot", response))
        clear_input()

# Display chat history
for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {msg}")

if __name__ == "__main__":
    main()
