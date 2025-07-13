import requests
from chatbot.utils import extract_complaint_id

class ComplaintAgent:
    def __init__(self, api_base):
        self.api_base = api_base
        self.fields = ['name', 'phone_number', 'email', 'complaint_details']
        self.collected = {}
        self.stage = 0

    def collect(self, user_input):
        # Complaint Retrieval Logic
        if "complaint" in user_input.lower() and "show" in user_input.lower():
            complaint_id = extract_complaint_id(user_input)
            if complaint_id:
                resp = requests.get(f"{self.api_base}/complaints/{complaint_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    return (
                        f"Complaint ID: {data['complaint_id']}\n"
                        f"Name: {data['name']}\n"
                        f"Phone: {data['phone_number']}\n"
                        f"Email: {data['email']}\n"
                        f"Details: {data['complaint_details']}\n"
                        f"Created At: {data['created_at']}"
                    )
                else:
                    return "Sorry, I couldn't find that complaint ID."
        
        # Complaint Creation Logic
