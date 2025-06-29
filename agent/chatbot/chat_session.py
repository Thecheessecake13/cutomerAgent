import requests
import re
from chatbot.rag_chain import rag_query
import streamlit as st

API_URL_CREATE = "http://127.0.0.1:8000/complaints"
API_URL_TRACK = "http://127.0.0.1:8000/complaints/{}"

class ChatSession:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = None  # None, "name", "phone", "email", "details"
        self.complaint = {}
        self.last_action = None

    def process(self, user_input):
        # Complaint tracking intent
        match = re.search(r"(complaint\s*ID[:\s]*)(\w+)", user_input, re.IGNORECASE)
        if ("show details" in user_input.lower() or "status" in user_input.lower()) and match:
            complaint_id = match.group(2)
            r = requests.get(API_URL_TRACK.format(complaint_id))
            if r.status_code == 200:
                data = r.json()
                self.reset()
                return (
                    f"Complaint ID: {data['complaint_id']}\n"
                    f"Name: {data['name']}\n"
                    f"Phone: {data['phone_number']}\n"
                    f"Email: {data['email']}\n"
                    f"Details: {data['complaint_details']}\n"
                    f"Created At: {data['created_at']}"
                )
            else:
                self.reset()
                return "Sorry, I couldn't find that complaint ID."

        # Complaint creation flow
        if self.state or "complaint" in user_input.lower():
            if not self.state:
                self.state = "name"
                self.complaint = {}
                return "I'm sorry to hear about your issue. Please provide your name."
            elif self.state == "name":
                self.complaint["name"] = user_input
                self.state = "phone"
                return f"Thank you, {user_input}. What is your phone number?"
            elif self.state == "phone":
                if re.match(r"^\+?\d{10,15}$", user_input):
                    self.complaint["phone_number"] = user_input
                    self.state = "email"
                    return "Got it. Please provide your email address."
                else:
                    return "Please enter a valid phone number (10-15 digits, optional +)."
            elif self.state == "email":
                if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
                    self.complaint["email"] = user_input
                    self.state = "details"
                    return "Thanks. Can you share more details about your complaint?"
                else:
                    return "Please enter a valid email address."
            elif self.state == "details":
                self.complaint["complaint_details"] = user_input
                r = requests.post(API_URL_CREATE, json=self.complaint)
                self.reset()
                if r.status_code == 200:
                    data = r.json()
                    return f"Your complaint has been registered with ID: {data['complaint_id']}. You'll hear back soon."
                else:
                    return "There was an error registering your complaint. Please try again."
        # RAG fallback
        return rag_query(user_input)

def clear_input():
    st.session_state.inp = ""

if "chat_session" not in st.session_state:
    # ... initialize session ...
    pass

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("📢 Grievance RAG Chatbot")

user_input = st.text_input("Type your message below:", key="inp")
if st.button("Send"):
    if user_input:
        response = st.session_state.chat_session.process(user_input)
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Bot", response))
        clear_input() 