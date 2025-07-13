import streamlit as st
from chatbot.chat_session import ChatSession
from chatbot.db import init_db
init_db()
from chatbot.db import insert_chat, fetch_chat_history, clear_chat_history



st.set_page_config(page_title="Customer Support Chatbot")
st.title(" Customer Support Chatbot")

#  User-defined backend
default_api_base = "http://127.0.0.1:8000"
api_base = st.text_input("Backend", value=default_api_base, key="api_base")


# Initialize session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession(api_base=st.session_state.api_base)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""


#  Fetch chat history from SQLite if session is empty
if not st.session_state.chat_history:
    history = fetch_chat_history()
    for _, sender, message in history:
        st.session_state.chat_history.append((sender, message))

#  Reset Button
if st.session_state.chat_history and any("Your complaint has been registered" in m for _, m in st.session_state.chat_history):
    if st.button("🔄 Reset Chat"):
        st.session_state.chat_session.reset()
        st.session_state.chat_history.clear()
        st.session_state.user_input = ""
        
        # Clear stored DB history too
        # clear_chat_history()
        st.rerun()

# Main input logic
def handle_input():
    query = st.session_state.user_input.strip()
    if query:
        st.session_state.chat_history.append(("You", query))
        insert_chat("You", query)

        try:
            response = st.session_state.chat_session.process(query)
            st.session_state.chat_history.append(("Bot", response))
            insert_chat("Bot", response)
        except Exception as e:
            err_msg = f"Error: {e}"
            st.session_state.chat_history.append(("Bot", err_msg))
            insert_chat("Bot", err_msg)
        finally:
            st.session_state.user_input = ""



# Input text field
st.text_input(
    "You:",
    key="user_input",
    placeholder="Type your complaint or ask a question...",
    on_change=handle_input,
    label_visibility="collapsed",
)

# Chat display
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
