import docker
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from utils.cerebras_client import analyze_logs_with_cerebras
from utils.llama_client import generate_recommendations
from fastapi.middleware.cors import CORSMiddleware
from utils.docker_mcp_mock import docker_mcp_mock
import asyncio

# --- Models ---
class ActionType(str, Enum):
    LOG_ANALYSIS = "log_analysis"
    RECOMMENDATION = "recommendation"
    DEPLOYMENT = "deployment"

class LogEntry(BaseModel):
    filename: str
    content: str

class LogRequest(BaseModel):
    logs: str

class ConversationContext(BaseModel):
    logs: List[LogEntry] = []
    analyses: List[str] = []
    currentTopic: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[ConversationContext] = None

class RecommendRequest(BaseModel):
    summary: str

class DeployRequest(BaseModel):
    service_name: str
    image: str

# --- App Setup ---
app = FastAPI(title="AI Ops Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to list of origins for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helpers ---
def make_response(action_type: ActionType, result: str):
    return {"type": action_type, "result": result}

# --- Endpoints ---
@app.post("/copilot-chat")
async def chat_endpoint(request: ChatRequest):
    try:
        message = (request.message or "").strip()
        context = request.context or ConversationContext()

        # Deploy command detection - USING MOCK MCP GATEWAY
        if "deploy" in message.lower():
            words = message.split()
            image_name = next((w for w in words if ":" in w), None)
            if not image_name and len(words) > 0:
                image_name = words[-1]

            if not image_name:
                return make_response(ActionType.DEPLOYMENT, "Error: No image name found in request")

            # Deploy via Docker MCP Gateway (mock)
            result = await docker_mcp_mock.deploy_container(
                image=image_name,
                name=f"service-{image_name.replace(':', '-').replace('.', '-')}",
                ports={'80/tcp': '8080'}
            )
            return make_response(ActionType.DEPLOYMENT, result)

        # List containers command
        if "list containers" in message.lower() or "show containers" in message.lower():
            result = await docker_mcp_mock.list_containers()
            return make_response(ActionType.DEPLOYMENT, result)

        # MCP status command
        if "mcp status" in message.lower() or "gateway status" in message.lower():
            result = await docker_mcp_mock.get_mcp_status()
            return make_response(ActionType.DEPLOYMENT, result)

        # Rest of your existing Cerebras and Llama logic remains unchanged...
        if any(w in message.lower() for w in ["error", "issue", "problem", "fail", "failure"]) and context and context.analyses:
            latest_analysis = context.analyses[-1]
            reco = generate_recommendations(f"Based on this log analysis: {latest_analysis}\nUser question: {request.message}")
            return make_response(ActionType.RECOMMENDATION, reco)

        # Default: ask LLaMA for a conversational/recommendation response
        resp = generate_recommendations(message)
        return make_response(ActionType.RECOMMENDATION, resp)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-logs")
async def analyze_logs(request: LogRequest):
    try:
        summary = analyze_logs_with_cerebras(request.logs)
        return make_response(ActionType.LOG_ANALYSIS, summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-logs-upload")
async def analyze_logs_upload(file: UploadFile = File(...)):
    try:
        logs = (await file.read()).decode("utf-8")
        summary = analyze_logs_with_cerebras(logs)
        return make_response(ActionType.LOG_ANALYSIS, summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend-actions")
async def recommend_actions(request: RecommendRequest):
    try:
        recommendations = generate_recommendations(request.summary)
        return make_response(ActionType.RECOMMENDATION, recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deploy")
async def deploy_service(req: DeployRequest):
    """Direct deploy endpoint using Docker MCP Gateway (mock)"""
    try:
        result = await docker_mcp_mock.deploy_container(
            image=req.image,
            name=req.service_name,
            ports={'80/tcp': '8080'}
        )
        return make_response(ActionType.DEPLOYMENT, result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
