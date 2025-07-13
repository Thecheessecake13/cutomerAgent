import ollama
from api.config import settings

_client = ollama.Client(host=settings.OLLAMA_HOST)

def generate_answer(message: str, history: list[dict]) -> str:
    resp = _client.chat(
        model=settings.OLLAMA_MODEL,
        messages=history + [{"role": "user", "content": message}],
        temperature=0.7
    )
    return resp.message.content
