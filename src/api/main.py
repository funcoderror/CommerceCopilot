
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
    print("CHAT REQUEST RECEIVED", flush=True)

    from src.tools.tool_calling import run_tool_assistant

    print("ASSISTANT IMPORTED SUCCESSFULLY", flush=True)

    response = run_tool_assistant(request.message)

    print("RESPONSE GENERATED", flush=True)

    return {"response": response}
