
A **Retrieval-Augmented Generation (RAG)**-powered chatbot that guides users through filing customer complaints via a REST API and answers follow-up questions using a small knowledge base.  

---

##  Project Structure

---
project/
├── api/ # FastAPI complaint + chat endpoints
│ ├── main.py
│ ├── routes.py
│ └── schemas.py
├── core/ # Database models & logic
│ ├── database.py
│ └── storage.py
├── chatbot/ # RAG chain + conversation flow
│ ├── rag_chain.py
│ └── conversation.py
├── data/ # Knowledge base files + FAISS store
│ └── kb/
│ ├── faqs.txt
│ └── policy.txt
│ └── faiss_store/ # Generated by ingestion
├── scripts/ # One-off ingestion & init scripts
│ └── ingest_kb.py
├── streamlit_app.py # Streamlit frontend
└── README.md # This file

##  Architecture & Flow

1. **Knowledge Base Ingestion**  
   - **Input**: Simple `.txt` FAQs and Policy files in `data/kb/`.  
   - **Processor**:  
     - Split text into chunks (300 char, 50 char overlap).  
     - Embed with HuggingFace’s `all-MiniLM-L6-v2`.  
     - Index in FAISS (persisted to `data/faiss_store`).  
   - **Script**: `scripts/ingest_kb.py`

2. **FastAPI Backend**  
   - **Database**: SQLite via SQLModel  
     - Table: `Complaint(complaint_id, name, phone_number, email, complaint_details, created_at)`  
     - Auto-migrated on startup (`core/database.py` → `init_db()`).  
   - **API Routes** (`api/routes.py`):  
     1. **POST /complaints**  
        - Input: `{ name, phone_number, email, complaint_details }`  
        - Action: store in DB, generate UUID complaint_id  
        - Output: `{ complaint_id, message }`  
     2. **GET /complaints/{complaint_id}**  
        - Fetch details by ID  
        - Output: full complaint record + timestamp  
     3. **POST /chat**  
        - Input: `{ query: string }`  
        - Internally uses the **Conversation flow** (below)  
        - Output: `{ answer: string, complaint_id?: string }`

3. **Conversation Flow** (`chatbot/conversation.py`)  
   - **States**:  
     1. **Collection**  
        - Prompts user sequentially for any missing fields:  
          1. “Please provide your name.”  
          2. “What is your phone number?”  
          3. “Please provide your email address.”  
          4. “Can you share more details about your complaint?”  
     2. **Registration**  
        - After all four are collected, calls POST `/complaints`  
        - Returns “Your complaint has been registered with ID: XYZ123…”  
     3. **Retrieval**  
        - If user query contains keywords like “show”/“status” and an ID pattern, calls GET `/complaints/{id}` and returns formatted details.  
     4. **RAG Fallback**  
        - For any other queries, runs a RAG chain that:  
          1. Uses FAISS to retrieve top-3 knowledge base chunks.  
          2. Prepends these as “Context” in the prompt.  
          3. Invokes Ollama LLM (e.g. `llama3`) to generate an answer.

4. **Streamlit Frontend** (`streamlit_app.py`)  
   - A simple chat UI that:  
     1. Collects user text via `st.chat_input`.  
     2. Shows conversation history.  
     3. On “Send”, POSTs `{ query }` to `/chat`.  
     4. Displays returned `answer`.  
   - Sidebar supports fetching complaint status by ID via GET `/complaints/{id}`.

---

## ⚙️ Setup Instructions

1. **Clone Repo**  
   ```bash
   git clone https://github.com/yourusername/grievance-rag-chatbot.git
   cd grievance-rag-chatbot
2. **Create & Activate Python venv
   ```bash
    python3 -m venv venv
    source venv/bin/activate

4. **Install Requirements
   ```bash
    pip install -r requirements.txt

6. ** Ingest Knowledge Base
   ```bash
    python scripts/ingest_kb.py
    # Verifies `data/faiss_store` is populated

5. **Start FastAPI Backend
   ```bash
    uvicorn api.main:app --reload --port 8000

7. **Run Streamlit Frontend
   ```bash
    streamlit run streamlit_app.py


Example Interaction

You: I want to file a complaint about a delayed delivery.
Bot: I’m sorry to hear that. Please provide your name.
You: Deepak
Bot: Thank you, Deepak. What is your phone number?
You: 1234567890
Bot: Got it. Please provide your email address.
You: deepak@example.com
Bot: Thanks. Can you share more details about the delayed delivery?
You: My order #12345 was supposed to arrive on May 1 but is still not here.
Bot: Your complaint has been registered with ID: 6f8b3e2a-d1c4-4aab-91c2-5f9e2d2b7d9f. You’ll hear back soon.

You: Show details for complaint 6f8b3e2a-d1c4-4aab-91c2-5f9e2d2b7d9f.
Bot:
Complaint ID: 6f8b3e2a-d1c4-4aab-91c2-5f9e2d2b7d9f  
Name: Deepak  
Phone: 1234567890  
Email: deepak@example.com  
Details: My order #12345 was supposed to arrive on May 1 but is still not here.  
Created At: 2025-06-28T14:32:10.123456  

