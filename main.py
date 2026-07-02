from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from agent import SHLAgent

# Initialize FastAPI
app = FastAPI(title="SHL Assessment Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ADD THE ROOT ENDPOINT RIGHT HERE (BEFORE agent initialization)
@app.get("/")
async def root():
    return {"message": "SHL Assessment Agent is running. Use /health or /chat endpoints."}

# Initialize agent
print("🚀 Starting SHL Assessment Agent...")
agent = SHLAgent()

# Request/Response models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation] = []
    end_of_conversation: bool = False

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Convert messages to dict
        messages = [msg.dict() for msg in request.messages]
        
        # Process through agent
        result = agent.process(messages)
        
        # Return formatted response
        return ChatResponse(
            reply=result['reply'],
            recommendations=result['recommendations'],
            end_of_conversation=result['end_of_conversation']
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)