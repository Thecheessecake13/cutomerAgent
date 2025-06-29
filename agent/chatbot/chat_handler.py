import requests

class ChatSession:
    def __init__(self):
        self.user_data = {
            "name": None,
            "phone_number": None,
            "email": None,
            "complaint_details": None,
        }
        self.awaiting_field = "name"

    def next_prompt(self):
        prompts = {
            "name": "Please provide your name.",
            "phone_number": "What is your phone number?",
            "email": "Got it. What's your email address?",
            "complaint_details": "Thanks. Can you describe your complaint?"
        }
        return prompts[self.awaiting_field]

    def update(self, user_input):
        for field in self.user_data:
            if self.user_data[field] is None:
                self.user_data[field] = user_input
                break
        for field in self.user_data:
            if self.user_data[field] is None:
                self.awaiting_field = field
                return False, self.next_prompt()
        return True, None

    def submit(self):
        response = requests.post("http://127.0.0.1:8001/complaints", json=self.user_data)
        if response.status_code == 200:
            return response.json()["complaint_id"]
        return None
