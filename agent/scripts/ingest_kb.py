# scripts/ingest_kb.py

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

def ingest_kb(
    source_dir: str = "data/kb",
    persist_path: str = "data/faiss_store"
):
    # 1) Load all .txt (or .pdf via PDFLoader) from data/kb/
    loader = DirectoryLoader(source_dir, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()

    # 2) Split into ~500-token overlapping chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    # 3) Embed & index with FAISS
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedder)

    # 4) Persist to disk
    os.makedirs(persist_path, exist_ok=True)
    vectorstore.save_local(persist_path)
    print(f"Ingested {len(chunks)} chunks into FAISS at {persist_path}")

if __name__ == "__main__":
    ingest_kb()
