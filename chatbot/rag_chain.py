

import os
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_ollama.llms import OllamaLLM
from langchain_objectbox.vectorstores import ObjectBox
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Constants
EMBED_DIM     = 384
OBJECTBOX_DIR = "/Users/annuahlawat/Desktop/agent/objectbox"
OLLAMA_MODEL  = "llama3"
EMBED_MODEL   = "sentence-transformers/all-MiniLM-L6-v2"

# Ensure the data directory exists
os.makedirs(OBJECTBOX_DIR, exist_ok=True)

# Singleton vectorstore
_vectorstore: ObjectBox | None = None

def ingest_knowledge_base(
    paths: List[str],
    embedding_model: str = EMBED_MODEL,
    embedding_dim: int = EMBED_DIM,
) -> ObjectBox:
    """
    Read documents from `paths`, split into chunks, embed, and store them.
    Returns a new vectorstore (used for one-time ingestion/testing).
    """
    # 1) Load + split
    docs = []
    for p in paths:
        loader = PyPDFLoader(p) if p.lower().endswith(".pdf") else TextLoader(p)
        docs.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 2) Embed + write into a fresh ObjectBox store
    embedding = HuggingFaceEmbeddings(model_name=embedding_model)
    vs = ObjectBox.from_texts(
        [chunk.page_content for chunk in chunks],
        embedding=embedding,
        embedding_dimensions=embedding_dim,
    )
    return vs

def _get_vectorstore() -> ObjectBox:
    """
    Lazily initialize and return the singleton ObjectBox store.
    """
    global _vectorstore
    if _vectorstore is None:
        embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        _vectorstore = ObjectBox(
            embedding=embedding,
            embedding_dimensions=EMBED_DIM,
        )
    return _vectorstore

def load_rag_chain(
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ollama_model: str = "llama3",
    embedding_dim: int = EMBED_DIM,
) -> RetrievalQA:
    embedding = HuggingFaceEmbeddings(model_name=embedding_model)

    # Directly initialize ObjectBox without from_existing_index
    vectorstore = ObjectBox(
        embedding=embedding,
        embedding_dimensions=embedding_dim,
    )
    print("[RAG] Initializing Ollama model...")

    llm = OllamaLLM(model=ollama_model)
    retriever = vectorstore.as_retriever()

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
    )


def rag_query(query: str) -> str:
    """
    Convenience one-shot wrapper around load_rag_chain().

    """
    print("[RAG] Loading chain...")
    chain = load_rag_chain()
    print("[RAG] Running query:", query)
    return chain.run(query)
    # chain = load_rag_chain()
    # return chain.run(query)
