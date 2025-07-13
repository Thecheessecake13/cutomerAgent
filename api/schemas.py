from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ComplaintCreate(BaseModel):
    name: str
    phone_number: str = Field(..., pattern=r"^\+?\d{10,15}$")

    email: EmailStr
    complaint_details: str

class ComplaintCreated(BaseModel):
    complaint_id: str
    message: str

class ComplaintRead(BaseModel):
    complaint_id: str
    name: str
    phone_number: str
    email: EmailStr
    complaint_details: str
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True 
