from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Ops Copilot")

class QueryRequest(BaseModel):
    query: str
    
class DeployRequest(BaseModel):
    service_name: str
    image: str

class LogRequest(BaseModel):
    logs: str 

@app.get("/")
def root():
    return {"message": "AI Ops Copilot Backend is running 🚀"}

@app.post("/query")
def query_ai(request: QueryRequest):
    """
    Meta Llama Integration Stub
    """
    return {
        "input": request.query,
        "response": f"Mock Llama response for: {request.query}"
    }

@app.post("/deploy")
def deploy_service(request: DeployRequest):
    """
    Docker MCP Gateway Stub
    """
    return {
        "service": request.service_name,
        "image": request.image,
        "status": "Deployment started (mock)"
    }

@app.post("/analyze-logs")
def analyze_logs(request: LogRequest):
    """
    Cerebras Log Analysis Stub
    """
    return {
        "logs_received": request.logs[:100],  # truncate preview
        "analysis": "Mock log summary: No critical errors detected."
    }