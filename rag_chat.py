# 

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import ollama

# 1) Load vectorstore from disk
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_PATH   = "data/faiss_store"

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vectorstore = FAISS.load_local(FAISS_PATH, embeddings)

# 2) Create Ollama client
client = ollama.Client()           
MODEL  = "llama2"                  

def rag_answer(user_question: str) -> str:
    # 3) Retrieve top–k docs
    docs_and_scores = vectorstore.similarity_search_with_score(
        user_question, k=3
    )
    contexts = "\n\n---\n\n".join(
        doc.page_content for doc,_ in docs_and_scores
    )

    # 4) Compose prompt
    system = {
        "role": "system",
        "content": (
            "You are a friendly customer-service assistant. "
            "Use the following policy excerpts to ground your answers:\n\n"
            f"{contexts}"
        )
    }
    user    = {"role": "user",    "content": user_question}

    # 5) Call Ollama as a chat model
    resp = client.chat(
        model=MODEL,
        messages=[system, user],
        temperature=0.1,
    )
    return resp.message.content

if __name__ == "__main__":
    while True:
        q = input("\nAsk something about our policies or file a complaint:\n> ")
        ans = rag_answer(q)
        print(f"\n {ans}\n")
