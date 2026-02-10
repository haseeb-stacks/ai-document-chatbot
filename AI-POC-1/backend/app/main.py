import sys
print("DEBUG: Starting main.py..."); sys.stdout.flush()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import sys

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag import rag_service

app = FastAPI(title="AI Document Chatbot")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str

# Initialize RAG on startup
@app.on_event("startup")
async def startup_event():
    rag_service.initialize()

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
            
        response = rag_service.chat(request.message)
        
        # Deduplicate sources
        unique_sources = list(set([os.path.basename(s) for s in response["sources"]]))
        
        return {
            "response": response["answer"],
            "sources": unique_sources
        }
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (Frontend)
# Try different common locations to be robust for Docker and local dev
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(base_dir, "frontend")

if not os.path.exists(frontend_path):
    # Fallback for Docker structure where backend is at /app/app
    docker_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_path = os.path.join(docker_base, "frontend")

print(f"DEBUG: Serving frontend from {frontend_path}"); sys.stdout.flush()

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    print(f"ERROR: Frontend path not found at {frontend_path}"); sys.stdout.flush()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
