# from datetime import datetime
# from sqlmodel import SQLModel, Field

# class Complaint(SQLModel, table=True):
#     complaint_id: str = Field(primary_key=True, index=True)
#     name: str
#     phone_number: str
#     email: str
#     complaint_details: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)


from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class Complaint(SQLModel, table=True):
    complaint_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    phone_number: str
    email: str
    complaint_details: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
