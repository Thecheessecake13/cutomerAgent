from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = FAISS.load_local("data/faiss_store", embedding_model, allow_dangerous_deserialization=True)
llm = Ollama(model="llama3")  # Make sure ollama is running

def rag_query(user_input):
    docs = vectordb.similarity_search(user_input, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = PromptTemplate.from_template(
        "Context:\n{context}\n\nUser: {user_input}\nBot:"
    )
    query = prompt.format(context=context, user_input=user_input)
    return llm.invoke(query)
