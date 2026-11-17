
from sentence_transformers import SentenceTransformer

print("Loading shared embedding model...", flush=True)

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)

print("Shared embedding model loaded!", flush=True)
