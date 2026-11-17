
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

import chromadb
from src.embedding_model import embedding_model


# 1. Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge_base"
DB_DIR = BASE_DIR / "chroma_db"


# 2. Load Groq API key
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Configure it in .env "
        "or Streamlit Cloud Secrets."
    )

groq_client = Groq(api_key=api_key)


# 3. Split documents into chunks
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


# 4. Initialize ChromaDB
client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_or_create_collection(
    name="commerce_knowledge",
    metadata={"hnsw:space": "cosine"}
)


# 5. Build knowledge base if empty
def initialize_knowledge_base():

    if collection.count() > 0:
        print(
            "Existing knowledge base loaded:",
            collection.count(),
            "chunks"
        )
        return

    print("Building knowledge base...")

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

    if not documents:
        raise ValueError(
            "No Markdown documents found in data/knowledge_base/. "
            "Make sure these files are committed to GitHub."
        )

    print("Total chunks created:", len(documents))

    # Generate embeddings using the shared model
    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True
    ).tolist()

    # Store in batches
    batch_size = 100

    for start in range(0, len(documents), batch_size):

        end = start + batch_size

        collection.upsert(
            ids=ids[start:end],
            documents=documents[start:end],
            embeddings=embeddings[start:end],
            metadatas=metadatas[start:end]
        )

    print(
        "Knowledge base initialized successfully:",
        collection.count(),
        "chunks"
    )


initialize_knowledge_base()


# 6. Retrieve relevant context
def retrieve_context(question, top_k=3):

    if collection.count() == 0:
        return ""

    question_embedding = embedding_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count())
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context


# 7. Build prompt
def build_prompt(question, context):

    prompt = f"""
You are CommerceCopilot, an AI shopping
and customer support assistant.

Answer the user's question using ONLY the
provided company knowledge base.

Rules:
1. Do not invent company policies.
2. If the answer is not available in the
   context, say you don't have enough
   information.
3. Keep answers clear and helpful.
4. Do not make assumptions.

COMPANY KNOWLEDGE:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    return prompt


# 8. Generate answer
def generate_answer(prompt):

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=500
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    question = input("\nYou: ")

    print("\nSearching company knowledge base...")

    context = retrieve_context(question)
    prompt = build_prompt(question, context)

    print("\nCommerceCopilot is thinking...\n")

    answer = generate_answer(prompt)

    print("=" * 60)
    print("             COMMERCE COPILOT")
    print("=" * 60)
    print("\n" + answer + "\n")
    print("=" * 60)
