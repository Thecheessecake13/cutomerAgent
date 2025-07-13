import os, numpy as np, faiss
from sentence_transformers import SentenceTransformer
from api.config import settings

_model = SentenceTransformer(settings.HF_EMBEDDING_MODEL)

class VectorStore:
    def __init__(self):
        self.dim        = settings.EMBEDDING_DIM
        self.index_path = settings.FAISS_INDEX_PATH
        self.ids_path   = self.index_path + ".ids.npy"

        # load or new
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            self.ids   = list(np.load(self.ids_path, allow_pickle=True))
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.ids   = []

    def add(self, docs: list[str], ids: list[str]):
        vecs = [ _model.encode(d, convert_to_numpy=True).astype("float32") for d in docs ]
        arr  = np.vstack(vecs)
        self.index.add(arr)
        self.ids.extend(ids)
        faiss.write_index(self.index, self.index_path)
        np.save(self.ids_path, np.array(self.ids, dtype=object))

    def query(self, text: str, top_k: int = 2) -> list[int]:
        qv = _model.encode(text, convert_to_numpy=True).astype("float32")
        D, I = self.index.search(qv.reshape(1, -1), top_k)
        return [int(i) for i in I[0] if i != -1]

vector_store = VectorStore()
