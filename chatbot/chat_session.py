
import logging
import requests
import random
import re
from chatbot.rag_chain import load_rag_chain

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")


class ChatSession:
    def __init__(self, api_base="http://127.0.0.1:8000"):
        self.api_base = api_base.rstrip("/")
        self.reset()
        self.rag_chain = load_rag_chain()

    def reset(self):
        self.awaiting = None  # Which field we're collecting next
        self.data = {}

    # def process(self, user_input: str) -> str:
        # user_input = user_input.strip()
        # print(f"[USER INPUT] {user_input}")  # Log input

        # id_match = re.search(r"\b([A-Z]{2,}\d+)\b", user_input)
        # if (("status" in user_input.lower() or "show details" in user_input.lower()) and id_match):
        #     return self._retrieve_complaint(id_match.group(1))

        # if self.awaiting:
        #     return self._handle_collection(user_input)

        # if any(kw in user_input.lower() for kw in ("file a complaint", "complaint", "register my complaint")):
        #     self.reset()
        #     self.awaiting = "name"
        #     return "I’m sorry to hear that. To get started, may I have your name?"

        # try:
        #     logging.debug("Sending to RAG chain...")
        #     print("[DEBUG] Triggering RAG query:", user_input)

        #     response = self.rag_chain.run(user_input)
        #     print(f"[LLM RESPONSE] {response}")  # Log LLM output
        #     return response
        # except Exception as e:
        #     print(f"[LLM ERROR] {e}")
        #     return "Sorry, I couldn’t process your question right now. Please try again later."
    def process(self, user_input: str) -> str:
        user_input = user_input.strip()
        print(f"[USER INPUT] {user_input}")

        # STEP 1: Handle complaint ID retrieval if ID is present
        id_match = re.search(r"\b([A-Z0-9]{6,})\b", user_input)
        if id_match and ("status" in user_input.lower() or "details" in user_input.lower()):
            return self._retrieve_complaint(id_match.group(1))

        # STEP 2: Continue collection flow if needed
        if self.awaiting:
            return self._handle_collection(user_input)

        # STEP 3: Start complaint flow
        if any(kw in user_input.lower() for kw in ("file a complaint", "register complaint", "raise complaint", "complaint about")):
            self.reset()
            self.awaiting = "name"
            return "I’m sorry to hear that. To get started, may I have your name?"

        # STEP 4: Fallback to RAG
        try:
            print("[DEBUG] Triggering RAG query:", user_input)
            response = self.rag_chain.run(user_input)
            print(f"[LLM RESPONSE] {response}")
            return response
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return "Sorry, I couldn’t process your question right now. Please try again later."

    def _handle_collection(self, user_input: str) -> str:
        # Name
        if self.awaiting == "name":
            self.data["name"] = user_input
            self.awaiting = "phone"
            return "Thank you. Now, please provide your phone number."

        # Phone
        if self.awaiting == "phone":
            if not re.match(r"^\+?\d{10,15}$", user_input):
                return "Please enter a valid phone number (10-15 digits, optional +)."
            self.data["phone_number"] = user_input
            self.awaiting = "email"
            return "Got it. What's your email address?"

        # Email
        if self.awaiting == "email":
            if not re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
                return "Please enter a valid email address."
            self.data["email"] = user_input
            self.awaiting = "details"
            return "Thanks. Could you please describe your complaint in detail?"

        # Details
        if self.awaiting == "details":
            self.data["complaint_details"] = user_input
            for attempt in range(5):  # Retry once
                try:
                    resp = requests.post(f"{self.api_base}/complaints", json=self.data, timeout=5)
                    resp.raise_for_status()
                    data = resp.json()
                    cid = data.get("complaint_id", "UNKNOWN")
                    self.reset()
                    return f"Your complaint has been registered successfully. Your complaint ID is **{cid}**."
                except requests.exceptions.RequestException as e:
                    logging.warning(f"[Attempt {attempt + 1}] Complaint submission failed: {e}")
                    if attempt == 1:
                        logging.error("Final complaint submission failed.")
                except Exception as e:
                    logging.exception("Unexpected error during complaint submission")
                    break
                    
            self.reset()
            return "Sorry, there was an error registering your complaint. Please try again later."

    def _retrieve_complaint(self, complaint_id: str) -> str:
        try:
            resp = requests.get(f"{self.api_base}/complaints/{complaint_id}")
            if resp.status_code == 404:
                self.reset()
                return f"I couldn’t find any complaint with ID {complaint_id}. Please check and try again."
            resp.raise_for_status()
            c = resp.json()

            status = c.get("status")
            if not status or status.strip() == "":
                status = random.choice(["Pending", "In Transit", "Completed", "On Hold"])

            # Apply formatting improvements here
            status = c.get("status") or "Pending"
            self.reset()
            return (
                f"Complaint ID: {c.get('complaint_id')}\n"
                f"Name: {c.get('name')}\n"
                f"Phone: {c.get('phone_number')}\n"
                f"Email: {c.get('email')}\n"
                f"Details: {c.get('complaint_details')}\n"
                f"Status: {status}\n"
                f"Created At: {c.get('created_at')}"
            )
        except Exception as e:
            logging.exception("Failed to retrieve complaint")
            self.reset()
            return "Sorry, I’m unable to fetch that complaint right now. Please try again later."

