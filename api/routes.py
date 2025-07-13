# # api/routes.py
# from fastapi import APIRouter, HTTPException
# # from schemas    import ComplaintCreate, ComplaintCreated, ComplaintRead
# from core.storage import save_complaint, get_complaint
# # Preferred: relative import within the api package
# from .schemas import ComplaintCreate, ComplaintCreated, ComplaintRead


# router = APIRouter(
#     prefix="/complaints",
#     tags=["Complaints"],
# )

# @router.post(
#     "/", 
#     response_model=ComplaintCreated,
#     summary="Create a new complaint"
# )
# def create_complaint(payload: ComplaintCreate):
#     saved = save_complaint(payload.dict())
#     return {"complaint_id": saved.complaint_id}

# @router.get(
#     "/{complaint_id}", 
#     response_model=ComplaintRead,
#     summary="Retrieve an existing complaint"
# )
# def read_complaint(complaint_id: str):
#     obj = get_complaint(complaint_id)
#     if obj is None:
#         raise HTTPException(status_code=404, detail="Complaint not found")
#     return obj




from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4
from datetime import datetime

from .models import Complaint
from .schemas import ComplaintCreate, ComplaintCreated, ComplaintRead
from .database import get_db

router = APIRouter()

@router.post("/complaints", response_model=ComplaintCreated)
async def create_complaint(
    complaint: ComplaintCreate,
    db: AsyncSession = Depends(get_db)
):
    # Generate unique complaint ID
    complaint_id = str(uuid4())[:8].upper()
    db_complaint = Complaint(
        complaint_id=complaint_id,
        name=complaint.name,
        phone_number=complaint.phone_number,
        email=complaint.email,
        complaint_details=complaint.complaint_details,
        created_at=datetime.utcnow(),
    )
    db.add(db_complaint)
    await db.commit()
    return {
        "complaint_id": complaint_id,
        "message": "Complaint created successfully"
    }

@router.get("/complaints/{complaint_id}", response_model=ComplaintRead)
async def get_complaint(
    complaint_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Complaint).where(Complaint.complaint_id == complaint_id))
    db_complaint = result.scalars().first()
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint
