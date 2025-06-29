# # api/schemas.py

# from pydantic import BaseModel, EmailStr, Field
# from datetime import datetime

# PHONE_PATTERN = r'^\+?\d{10,15}$'

# # ------------ Complaint schemas ------------

# class ComplaintCreate(BaseModel):
#     name: str = Field(..., example="John Doe")
#     phone_number: str = Field(
#         ..., 
#         example="+1234567890", 
#         pattern=PHONE_PATTERN,
#         description="10–15 digits, optionally prefixed with +"
#     )
#     email: EmailStr = Field(..., example="john.doe@example.com")
#     complaint_details: str = Field(..., example="I cannot log in.")

# class ComplaintCreated(BaseModel):
#     complaint_id: str
#     message: str = "Complaint created successfully"

# class ComplaintRead(BaseModel):
#     complaint_id: str
#     name: str
#     phone_number: str
#     email: EmailStr
#     complaint_details: str
#     created_at: datetime

# # ------------ Chat schemas ------------

# from typing import Optional, Dict

# class QueryRequest(BaseModel):
#     message: str
#     context: Dict[str, str] = {}
#     name: Optional[str]
#     phone_number: Optional[str]
#     email: Optional[str]
#     complaint_details: Optional[str]

# class QueryResponse(BaseModel):
#     answer: str
#     context: Dict[str, str]
#     complete: bool
#     complaint_id: Optional[str] = None


from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    name: str
    phone_number: str = Field(..., pattern=r'^\+?\d{10,15}$')
    email: EmailStr
    complaint_details: str

class ComplaintCreated(BaseModel):
    complaint_id: str
    message: str = "Complaint created successfully"

class ComplaintRead(BaseModel):
    complaint_id: str
    name: str
    phone_number: str
    email: str
    complaint_details: str
    created_at: datetime
