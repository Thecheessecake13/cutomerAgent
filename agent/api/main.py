# from fastapi import FastAPI
# from api.routes import router

# app = FastAPI(
#     title="Grievance RAG Chatbot API",
#     description="Handles complaint creation and retrieval",
#     version="1.0.0"
# )

# app.include_router(router, prefix="/api")

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Grievance RAG Chatbot API"}


from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Grievance RAG Chatbot API")

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Grievance RAG Chatbot API"}
