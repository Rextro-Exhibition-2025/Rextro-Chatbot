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
os.environ["GEMINI_API_KEY"] = config.gemini_api_key

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
    pass

# --- Endpoints ---
@app.post("/ask", response_model=QueryResponse)
@limiter.limit("100/5seconds")
async def ask_agent(request: Request, query_request: QueryRequest):
    """Endpoint to interact with the RAG agent. Limited to 5 requests per 2 seconds."""
    
    try:
        response_data = await run_agent_async(query_request.query)
        
        answer = response_data.answer if hasattr(response_data, 'answer') else str(response_data)
        
        result = {"answer": answer}
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        # Return error response
        error_response = {"answer": f"I encountered an error while processing your request: {str(e)}. Please try again or contact support."}
        return error_response

@app.get("/")
async def health_check():
    """Health check endpoint with 10s delay."""
    await asyncio.sleep(15)
    response = {"status": "ok", "message": "Agentic RAG API is running"}
    return response

# --- Main Execution ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)