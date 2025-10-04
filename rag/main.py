import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from config.config import get_config
from src.agent.agent import run_agent_async
import os
from fastapi.middleware.cors import CORSMiddleware

# --- Configuration ---
config = get_config()
os.environ["OPENAI_API_KEY"] = config.openai_api_key

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Agentic RAG API",
    description="Simplified FastAPI server for Agentic RAG system",
    version="1.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

# --- Event Handlers ---
@app.on_event("startup")
async def startup_event():
    print("🚀 Agentic RAG API started successfully!")
    print("📡 Running on http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")

# --- Endpoints ---
@app.post("/ask", response_model=QueryResponse)
async def ask_agent(request: QueryRequest):
    """Endpoint to interact with the RAG agent."""
    print(f"Received query: {request.query}")
    response_data = await run_agent_async(request.query)

    answer = response_data.answer if hasattr(response_data, 'answer') else str(response_data)
    return {"answer": answer}

@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Agentic RAG API is running"}

# --- Main Execution ---
if __name__ == "__main__":
    import uvicorn
    print("🔥 Starting Simplified Agentic RAG API Server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
