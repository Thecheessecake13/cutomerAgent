
import requests
from utils import extract_complaint_id  # your single regex helper

class ComplaintAgent:
    def __init__(self, rag_chain, api_base="http://127.0.0.1:8001"):
        self.rag_chain   = rag_chain
        self.api_base    = api_base
        self.fields      = ["name", "phone", "email", "details"]
        self.data        = {}          # collected field values
        self.awaiting    = None        # which field to ask next
        self.submitted   = False       # whether we’ve called POST

    def process(self, user_input: str) -> str:
        # 1) Retrieval take-priority: look for complaint ID anywhere
        cid = extract_complaint_id(user_input)
        if cid:
            return self._retrieve_complaint(cid)

        # 2) Are we mid-collection (awaiting a field)?
        if self.awaiting:
            # store the answer
            self.data[self.awaiting] = user_input.strip()
            # clear awaiting if done, or set to next
            next_field = self._next_missing_field()
            if next_field:
                self.awaiting = next_field
                return f"Thanks. What's your {next_field}?"
            else:
                # all done → submit
                return self._submit_complaint()

        # 3) Fresh “start complaint” detection
        if "complaint" in user_input.lower() or "file a complaint" in user_input.lower():
            self.data.clear()
            self.submitted = False
            # kick off with first field
            self.awaiting = self.fields[0]
            return f"Sure—I can help with that. First, may I have your {self.awaiting}?"

        # 4) Fallback to RAG for any other query
        return self.rag_chain.run(user_input)

    def _next_missing_field(self) -> str | None:
        for f in self.fields:
            if f not in self.data:
                return f
        return None

    def _submit_complaint(self) -> str:
        payload = {
            "name":    self.data["name"],
            "phone":   self.data["phone"],
            "email":   self.data["email"],
            "details": self.data["details"],
        }
        resp = requests.post(f"{self.api_base}/complaints", json=payload)
        resp.raise_for_status()
        cid = resp.json().get("complaint_id")
        # reset for next time
        self.awaiting  = None
        self.submitted = True
        self.data.clear()
        return f"Your complaint has been registered successfully. Your complaint ID is **{cid}**."

    def _retrieve_complaint(self, complaint_id: str) -> str:
        resp = requests.get(f"{self.api_base}/complaints/{complaint_id}")
        if resp.status_code == 404:
            return f"I couldn’t find any complaint with ID {complaint_id}. Please check the ID and try again."
        resp.raise_for_status()
        c = resp.json()
        # Format the returned JSON into a friendly message
        return (
            f"Here are the details for complaint **{complaint_id}**:\n\n"
            f"- **Name:** {c.get('name')}\n"
            f"- **Phone:** {c.get('phone')}\n"
            f"- **Email:** {c.get('email')}\n"
            f"- **Details:** {c.get('details')}\n"
            f"- **Status:** {c.get('status')}\n"
            f"- **Created at:** {c.get('created_at')}"
        )
