from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Complaint(Base):
    __tablename__ = "complaints"
    complaint_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    complaint_details = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
