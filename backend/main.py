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
    conversationHistory: List[dict] = []  #this is to track conversation history
    recentMessages: List[dict] = []  # and this is for recent messages from frontend

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
        
        # Build context-aware prompt
        context_prompt = self._build_context_prompt(message, context)
        
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
            
            # Update context
            context.conversationHistory.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": result}
            ])
            
            return {
                "type": ActionType.DEPLOYMENT, 
                "result": result,
                "context": context  # Return updated context
            }

        # List containers command
        if "list containers" in message.lower() or "show containers" in message.lower():
            result = await docker_mcp_mock.list_containers()
            
            # Update context
            context.conversationHistory.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": result}
            ])
            
            return {
                "type": ActionType.DEPLOYMENT, 
                "result": result,
                "context": context
            }

        # MCP status command
        if "mcp status" in message.lower() or "gateway status" in message.lower():
            result = await docker_mcp_mock.get_mcp_status()
            
            # Update context
            context.conversationHistory.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": result}
            ])
            
            return {
                "type": ActionType.DEPLOYMENT, 
                "result": result,
                "context": context
            }

        # If the message looks like a follow-up about issues and we have prior analyses, use LLaMA as recommender
        if any(w in message.lower() for w in ["error", "issue", "problem", "fail", "failure"]) and context and context.analyses:
            latest_analysis = context.analyses[-1]
            
            # Build context-aware prompt
            prompt = f"""
            Conversation Context:
            {self._format_conversation_history(context.conversationHistory[-4:])}  # Last 2 exchanges
            
            Log Analysis Context: {latest_analysis}
            
            Current User Question: {message}
            
            Based on the above conversation and log analysis, provide specific recommendations:
            """
            
            reco = generate_recommendations(prompt)
            
            # Update context
            context.conversationHistory.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": reco}
            ])
            
            return {
                "type": ActionType.RECOMMENDATION, 
                "result": reco,
                "context": context
            }

        # Default: ask LLaMA with conversation context
        prompt = f"""
        Conversation History:
        {self._format_conversation_history(context.conversationHistory[-6:])}  # Last 3 exchanges
        
        Current Message: {message}
        
        Please provide a helpful response that continues the conversation naturally:
        """
        
        resp = generate_recommendations(prompt)
        
        # Update context
        context.conversationHistory.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": resp}
        ])
        
        return {
            "type": ActionType.RECOMMENDATION, 
            "result": resp,
            "context": context
        }

        # resp = generate_recommendations(message)
        # return make_response(ActionType.RECOMMENDATION, resp)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def _build_context_prompt(self, message: str, context: ConversationContext) -> str:
    """Build a context-aware prompt for the AI"""
    prompt_parts = []
    
    # Add recent conversation history
    if context.conversationHistory:
        prompt_parts.append("Recent conversation:")
        for msg in context.conversationHistory[-6:]:  # Last 3 exchanges
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt_parts.append(f"{role}: {msg['content']}")
    
    # Add log analyses if relevant
    if context.analyses and any(word in message.lower() for word in ["log", "error", "issue", "analysis"]):
        prompt_parts.append(f"\nPrevious log analysis: {context.analyses[-1]}")
    
    prompt_parts.append(f"\nCurrent user message: {message}")
    prompt_parts.append("\nPlease provide a helpful response that considers the conversation context:")
    
    return "\n".join(prompt_parts)

def _format_conversation_history(self, history: List[dict]) -> str:
    """Format conversation history for the prompt"""
    if not history:
        return "No previous conversation."
    
    formatted = []
    for msg in history:
        role = "User" if msg.get("role") == "user" else "Assistant"
        formatted.append(f"{role}: {msg.get('content', '')}")
    
    return "\n".join(formatted)

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
