import docker
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from utils.cerebras_client import analyze_logs_with_cerebras
from fastapi import UploadFile, File
from utils.llama_client import generate_recommendations



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
    Deploy container using Docker SDK (MCP-ready).
    """
    try:
        client = docker.from_env()
        container = client.containers.run(
            request.image,
            name=request.service_name,
            detach=True,
            ports={"6379/tcp": 6379} if "redis" in request.image else None
        )
        return {
            "service": request.service_name,
            "image": request.image,
            "status": "Running",
            "container_id": container.id[:12]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-logs")
def analyze_logs(request: LogRequest):
    summary = analyze_logs_with_cerebras(request.logs)
    return {
        "logs_received": request.logs[:100] + "...",
        "analysis": summary
    }


@app.post("/analyze-logs-upload")
async def analyze_logs_upload(file: UploadFile = File(...)):
    logs = (await file.read()).decode("utf-8")
    summary = analyze_logs_with_cerebras(logs)
    return {
        "logs_received": logs[:100] + "...",
        "analysis": summary
    }
    
@app.post("/recommend-actions")
def recommend_actions(request: LogRequest):
    summary = analyze_logs_with_cerebras(request.logs)  # Step 1: Cerebras analysis
    recommendations = generate_recommendations(summary) # Step 2: LLaMA recommendations
    return {
        "analysis": summary,
        "recommendations": recommendations
    }