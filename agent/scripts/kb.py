# scripts/ingest_kb.py

import os
from pathlib import Path
from core.embeddings import get_embedding
from chromadb.config import Settings as ChromaSettings
import chromadb

# Adjust to faiss if you prefer
client = chromadb.Client(ChromaSettings())
collection = client.get_or_create_collection("kb")

def ingest_directory(dir_path: str):
    for file in Path(dir_path).glob("*.txt"):
        text = file.read_text(encoding="utf-8")
        emb = get_embedding(text)
        collection.add(
            documents=[text],
            embeddings=[emb],
            metadatas=[{"source": file.name}],
            ids=[str(file.name)]
        )
    print(f"Ingested {len(list(Path(dir_path).glob('*.txt')))} documents.")

if __name__ == "__main__":
    ingest_directory("data/kb")
