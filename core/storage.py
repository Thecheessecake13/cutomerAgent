
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
# from .config import settings
# from api.config import settings
from api.config import DB_URL

# 1) Set up engine & session
# for SQLite only; remove connect_args for other databases
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# 2) Define ORM model
class Complaint(Base):
    __tablename__ = "complaints"
    id               = Column(Integer, primary_key=True, index=True)
    complaint_id     = Column(String, unique=True, index=True, nullable=False)
    name             = Column(String, nullable=False)
    phone_number     = Column(String, nullable=False)
    email            = Column(String, nullable=False)
    complaint_details= Column(String, nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow)

# 3) Create tables
Base.metadata.create_all(bind=engine)

# 4) CRUD helpers
def save_complaint(data: dict) -> Complaint:
    """
    Inserts a new complaint and returns the ORM object.
    """
    db = SessionLocal()
    # generate a unique ID, e.g. 'CMP' + 8 hex chars
    complaint_id = "CMP" + uuid.uuid4().hex[:8].upper()
    db_obj = Complaint(complaint_id=complaint_id, **data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    db.close()
    return db_obj

def get_complaint(complaint_id: str) -> Complaint | None:
    """
    Fetches a complaint by its complaint_id.
    """
    db = SessionLocal()
    obj = db.query(Complaint).filter_by(complaint_id=complaint_id).first()
    db.close()
    return obj
