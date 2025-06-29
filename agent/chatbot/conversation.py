# conversation.py
import requests
from chatbot.rag_chain import load_rag_chain

API_BASE = "http://127.0.0.1:8001/api/complaints"

class ChatSession:
    def __init__(self):
        self.qa_chain = load_rag_chain()
        self.user_data = {"name": "", "phone_number": "", "email": "", "complaint_details": ""}
        self.awaiting = "complaint"  # states: complaint, name, phone, email
        self.complaint_id = ""

    def process_input(self, user_input):
        # Check if it's a complaint ID query
        if "complaint" in user_input.lower() and any(x in user_input.lower() for x in ["show", "status", "details", "retrieve"]):
            comp_id = self._extract_complaint_id(user_input)
            return self.get_complaint(comp_id)

        # Collect missing info in flow
        if self.awaiting == "complaint":
            self.user_data["complaint_details"] = user_input
            self.awaiting = "name"
            return "I'm sorry to hear that. Could you please provide your name?"

        elif self.awaiting == "name":
            self.user_data["name"] = user_input
            self.awaiting = "phone"
            return f"Thank you, {user_input}. What is your phone number?"

        elif self.awaiting == "phone":
            self.user_data["phone_number"] = user_input
            self.awaiting = "email"
            return "Got it. Please provide your email address."

        elif self.awaiting == "email":
            self.user_data["email"] = user_input
            return self.register_complaint()

        # Otherwise fallback to RAG
        return self.qa_chain.run(user_input)

    def register_complaint(self):
        try:
            response = requests.post(API_BASE, json=self.user_data)
            data = response.json()
            self.complaint_id = data.get("complaint_id", "")
            return f"Your complaint has been registered with ID: {self.complaint_id}. You'll hear back soon."
        except Exception as e:
            return "Failed to register complaint. Please try again."

    def get_complaint(self, comp_id):
        try:
            response = requests.get(f"{API_BASE}/{comp_id}")
            if response.status_code == 200:
                data = response.json()
                return (
                    f"Complaint ID: {data['complaint_id']}\n"
                    f"Name: {data['name']}\n"
                    f"Phone: {data['phone_number']}\n"
                    f"Email: {data['email']}\n"
                    f"Details: {data['complaint_details']}\n"
                    f"Created At: {data['created_at']}"
                )
            return "Complaint not found."
        except:
            return "Could not retrieve the complaint. Please try again later."

    def _extract_complaint_id(self, text):
        words = text.split()
        for word in words:
            if len(word) >= 6 and word.upper().startswith("XYZ"):
                return word
        return ""
