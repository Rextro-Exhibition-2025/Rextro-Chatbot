import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from config.config import get_config
from src.agent.agent import run_agent_async
import os
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# --- Configuration ---
config = get_config()
os.environ["OPENAI_API_KEY"] = config.openai_api_key

# --- Rate Limiter Setup ---
limiter = Limiter(key_func=get_remote_address)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Agentic RAG API",
    description="Simplified FastAPI server for Agentic RAG system",
    version="1.0.0"
)

# --- Add Rate Limiter to App ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
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
@limiter.limit("100/5seconds")
async def ask_agent(request: Request, query_request: QueryRequest):
    """Endpoint to interact with the RAG agent. Limited to 5 requests per 2 seconds."""
    print(f"Received query: {query_request.query}")
    response_data = await run_agent_async(query_request.query)

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