from fastapi import APIRouter, HTTPException
from api.schemas import ComplaintCreate, ComplaintCreated, ComplaintRead
from core.storage import save_complaint, get_complaint

# router = APIRouter()
router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)

@router.post("/complaints", response_model=ComplaintCreated)
def create_complaint(complaint: ComplaintCreate):
    saved = save_complaint(complaint.dict())
    return {"complaint_id": saved.complaint_id, "message": "Complaint created successfully"}

@router.get("/complaints/{complaint_id}", response_model=ComplaintRead)
def read_complaint(complaint_id: str):
    complaint = get_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint
