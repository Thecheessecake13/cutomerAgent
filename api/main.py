# from fastapi import FastAPI
# from api.routes import router

# app = FastAPI(
#     title="Grievance RAG Chatbot API",
#     version="1.0.0",
#     description="Handles complaint creation and retrieval"
# )
# app.include_router(router, prefix="/api")


from fastapi import FastAPI
from .routes import router
from .models import Base
from .database import engine

app = FastAPI(title="Complaint API")
app.include_router(router)

# Create tables at startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
