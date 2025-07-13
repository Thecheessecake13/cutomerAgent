from sqlmodel import SQLModel, create_engine, Session
from api.config import settings

engine = create_engine(settings.DB_URL, echo=True)

def init_db():
    """Create DB & tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Sync session factory."""
    with Session(engine) as session:
        yield session
