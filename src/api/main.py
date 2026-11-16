
from fastapi import FastAPI
from pydantic import BaseModel

from src.tools.tool_calling import run_tool_assistant

app = FastAPI(title="CommerceCopilot API")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "CommerceCopilot API is running!"}


@app.post("/chat")
def chat(request: ChatRequest):

    response = run_tool_assistant(request.message)

    return {"response": response}
