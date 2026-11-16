
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# 1. Set project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge_base"
DB_DIR = BASE_DIR / "chroma_db"


# 2. Load the embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# 3. Split documents into smaller chunks
def split_into_chunks(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []

    for start in range(0, len(words), chunk_size - overlap):
        chunk_words = words[start:start + chunk_size]

        if not chunk_words:
            break

        chunks.append(" ".join(chunk_words))

        if start + chunk_size >= len(words):
            break

    return chunks


# 4. Read all knowledge-base documents
documents = []
metadatas = []
ids = []

for file_path in KNOWLEDGE_DIR.glob("*.md"):

    text = file_path.read_text(encoding="utf-8")
    chunks = split_into_chunks(text)

    for index, chunk in enumerate(chunks):

        documents.append(chunk)

        metadatas.append({
            "source": file_path.name,
            "chunk": index
        })

        ids.append(f"{file_path.stem}_{index}")


print(f"\nTotal chunks created: {len(documents)}")

if not documents:
    raise ValueError("No documents were loaded!")


# 5. Generate embeddings
print("\nGenerating embeddings...")

embeddings = model.encode(
    documents,
    normalize_embeddings=True
).tolist()

print("Embeddings generated!")


# 6. Initialize ChromaDB
client = chromadb.PersistentClient(
    path=str(DB_DIR)
)

collection = client.get_or_create_collection(
    name="commerce_knowledge",
    metadata={"hnsw:space": "cosine"}
)


# 7. Store documents and embeddings
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("\nKnowledge base stored in ChromaDB!")
print("Total stored records:", collection.count())


# 8. Semantic search function
def search_knowledge(query, top_k=3):

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    print("\nSearch query:", query)
    print("\nRelevant results:\n")

    for i, document in enumerate(results["documents"][0]):

        source = results["metadatas"][0][i]["source"]
        distance = results["distances"][0][i]

        print(f"Result {i + 1}")
        print("Source:", source)
        print("Distance:", round(distance, 4))
        print("Content:", document)
        print("-" * 50)


# 9. Test semantic search
if collection.count() > 0:
    search_knowledge(
        "Can I get my money back if I don't like the product?"
    )

    search_knowledge(
        "How long will my order take to arrive?"
    )

    search_knowledge(
        "What if my product arrives damaged?"
    )
else:
    print("No documents found in the collection.")
