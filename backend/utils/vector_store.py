import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []


def add_to_index(embedding, doc_id):
    vector = np.array([embedding]).astype("float32")
    index.add(vector)
    documents.append(doc_id)


def search(query_embedding, k=3):
    if len(documents) == 0:
        return []   # 🔥 prevent crash

    vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(vector, k)

    results = []
    for i in indices[0]:
        if i < len(documents):
            results.append(documents[i])

    return results