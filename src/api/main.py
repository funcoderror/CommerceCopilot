
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CommerceCopilot API")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "CommerceCopilot API is running!"}


@app.post("/chat")
def chat(request: ChatRequest):

    print("STEP 1: CHAT REQUEST RECEIVED", flush=True)

    print("STEP 2: IMPORTING TOOL CALLING", flush=True)

    import json
    print("STEP 3: JSON IMPORTED", flush=True)

    from src.rag import rag_pipeline
    print("STEP 4: RAG PIPELINE IMPORTED", flush=True)

    from src.tools import tools
    print("STEP 5: TOOLS MODULE IMPORTED", flush=True)

    from src.memory import chat_memory
    print("STEP 6: CHAT MEMORY IMPORTED", flush=True)

    print("STEP 7: IMPORTING ASSISTANT", flush=True)

    from src.tools.tool_calling import run_tool_assistant

    print("STEP 8: ASSISTANT IMPORTED SUCCESSFULLY", flush=True)

    response = run_tool_assistant(request.message)

    print("STEP 9: RESPONSE GENERATED", flush=True)

    return {"response": response}
