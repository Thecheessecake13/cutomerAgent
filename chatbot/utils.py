
import re

def extract_complaint_id(text: str) -> str:
    match = re.search(r"\b([A-Z]{3}\d{4,})\b", text)
    return match.group(1) if match else ""
