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
print("🔧 Loading configuration...")
config = get_config()
print(f"🔑 OpenAI API Key loaded: {'✅' if config.openai_api_key else '❌'}")
os.environ["OPENAI_API_KEY"] = config.openai_api_key
print("📋 Configuration loaded successfully")

# --- Rate Limiter Setup ---
print("⏱️ Setting up rate limiter...")
limiter = Limiter(key_func=get_remote_address)
print("✅ Rate limiter configured")

# --- FastAPI App Initialization ---
print("🏗️ Initializing FastAPI app...")
app = FastAPI(
    title="Agentic RAG API",
    description="Simplified FastAPI server for Agentic RAG system",
    version="1.0.0"
)
print("✅ FastAPI app initialized")

# --- Add Rate Limiter to App ---
print("🛡️ Adding rate limiter to app...")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
print("✅ Rate limiter exception handler added")

# --- CORS Middleware ---
print("🌐 Setting up CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✅ CORS middleware configured")

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
    print(f"🔍 [DEBUG] Received query: {query_request.query}")
    print(f"🌐 [DEBUG] Request IP: {get_remote_address(request)}")
    
    try:
        print("🤖 [DEBUG] Starting agent processing...")
        response_data = await run_agent_async(query_request.query)
        print(f"📋 [DEBUG] Raw agent response type: {type(response_data)}")
        print(f"📋 [DEBUG] Raw agent response: {response_data}")
        
        # Debug response attribute checking
        print(f"🔍 [DEBUG] Has 'answer' attribute: {hasattr(response_data, 'answer')}")
        if hasattr(response_data, 'answer'):
            print(f"📝 [DEBUG] Answer attribute value: {response_data.answer}")
        
        answer = response_data.answer if hasattr(response_data, 'answer') else str(response_data)
        print(f"✅ [DEBUG] Final answer: {answer}")
        
        result = {"answer": answer}
        print(f"📤 [DEBUG] Returning response: {result}")
        return result
        
    except Exception as e:
        print(f"❌ [ERROR] Exception in ask_agent: {type(e).__name__}: {str(e)}")
        print(f"❌ [ERROR] Exception details: {repr(e)}")
        import traceback
        print(f"🔴 [ERROR] Full traceback:\n{traceback.format_exc()}")
        
        # Return error response
        error_response = {"answer": f"I encountered an error while processing your request: {str(e)}. Please try again or contact support."}
        print(f"🚨 [DEBUG] Error response: {error_response}")
        return error_response

@app.get("/")
async def health_check():
    """Health check endpoint with 10s delay."""
    print("🏥 [DEBUG] Health check endpoint called")
    print("⏳ [DEBUG] Starting 15 second delay...")
    await asyncio.sleep(15)
    print("✅ [DEBUG] Health check delay completed")
    response = {"status": "ok", "message": "Agentic RAG API is running"}
    print(f"📤 [DEBUG] Health check response: {response}")
    return response

# --- Main Execution ---
if __name__ == "__main__":
    import uvicorn
    print("🔥 Starting Simplified Agentic RAG API Server...")
    print("🚀 [DEBUG] About to start uvicorn server...")
    print("🌐 [DEBUG] Server config: host=0.0.0.0, port=8000, reload=True")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)