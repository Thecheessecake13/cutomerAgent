# import uuid
# from fastapi import HTTPException, status
# from sqlmodel import select
# from core.models import Complaint
# from core.database import get_session

# def save_complaint(name: str, phone_number: str, email: str, complaint_details: str) -> Complaint:
#     complaint_id = uuid.uuid4().hex
#     comp = Complaint(
#         complaint_id=complaint_id,
#         name=name,
#         phone_number=phone_number,
#         email=email,
#         complaint_details=complaint_details,
#     )
#     with next(get_session()) as session:
#         session.add(comp)
#         session.commit()
#         session.refresh(comp)
#     return comp

# def get_complaint(complaint_id: str) -> Complaint:
#     with next(get_session()) as session:
#         comp = session.exec(select(Complaint).where(Complaint.complaint_id == complaint_id)).one_or_none()
#         if not comp:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Complaint {complaint_id} not found"
#             )
#         return comp


from sqlmodel import Session
from core.database import engine
from core.models import Complaint

def save_complaint(complaint_data):
    with Session(engine) as session:
        complaint = Complaint(**complaint_data)
        session.add(complaint)
        session.commit()
        session.refresh(complaint)
        return complaint

def get_complaint(complaint_id: str):
    with Session(engine) as session:
        complaint = session.get(Complaint, complaint_id)
        return complaint
