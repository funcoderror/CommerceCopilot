
import os
from dotenv import load_dotenv
from groq import Groq

from pathlib import Path

import chromadb
from src.embedding_model import embedding_model


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

groq_client = Groq(api_key=api_key)

DB_DIR = BASE_DIR / "chroma_db"

# Connect to existing ChromaDB
client = chromadb.PersistentClient(path=str(DB_DIR))

collections = client.list_collections()

if not collections:
    raise ValueError("No ChromaDB collections found. Run Day 3 first.")

# Reuse the collection created on Day 3
collection_name = (
    collections[0].name
    if hasattr(collections[0], "name")
    else collections[0]
)

collection = client.get_collection(name=collection_name)

print("Connected to knowledge base:", collection_name)


def retrieve_context(question, top_k=3):

    # Convert question into embedding
    question_embedding = embedding_model.encode(
        question
    ).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count())
    )

    documents = results["documents"][0]

    # Combine retrieved chunks
    context = "\n\n".join(documents)

    return context


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

    answer = response.choices[0].message.content

    return answer



if __name__ == "__main__":

    question = input("\nYou: ")

    print("\nSearching company knowledge base...")

    # Step 1: Retrieve relevant information
    context = retrieve_context(question)

    # Step 2: Construct the prompt
    prompt = build_prompt(question, context)

    # Step 3: Generate answer using Groq
    print("\nCommerceCopilot is thinking...\n")

    answer = generate_answer(prompt)

    # Step 4: Display final response
    print("=" * 60)
    print("             COMMERCECOPILOT")
    print("=" * 60)

    print("\n" + answer + "\n")

    print("=" * 60)
