@app.post("/chat")
def chat(request: ChatRequest):
    print("CHAT REQUEST RECEIVED", flush=True)

    from src.tools.tool_calling import run_tool_assistant

    print("ASSISTANT IMPORTED SUCCESSFULLY", flush=True)

    response = run_tool_assistant(request.message)

    print("RESPONSE GENERATED", flush=True)

    return {"response": response}