import asyncio
import random
from typing import Dict, Any
import uuid
from datetime import datetime

class DockerMCPMockClient:
    """
    Mock Docker MCP Gateway client for hackathon demonstration.
    Simulates the MCP protocol and Docker operations.
    """
    
    def __init__(self):
        self.containers = {}
        self.images = ["nginx:latest", "redis:alpine", "postgres:13", "node:18", "python:3.9"]
        self.mcp_version = "1.0.0"
        
    async def initialize_mcp_session(self) -> Dict[str, Any]:
        """Simulate MCP handshake"""
        return {
            "protocolVersion": self.mcp_version,
            "capabilities": {
                "containers": ["create", "start", "stop", "list"],
                "images": ["pull", "list"],
                "networks": ["create", "list"]
            },
            "serverInfo": {
                "name": "docker-mcp-gateway",
                "version": "0.1.0"
            }
        }
    
    async def deploy_container(self, image: str, name: str, ports: Dict[str, str] = None) -> str:
        """
        Mock container deployment using MCP protocol pattern
        """
        try:
            # Simulate MCP method call
            mcp_request = {
                "jsonrpc": "2.0",
                "method": "docker/container/create",
                "params": {
                    "image": image,
                    "name": name,
                    "ports": ports or {},
                    "detach": True
                },
                "id": str(uuid.uuid4())
            }
            
            # Simulate network delay
            await asyncio.sleep(1.5)
            
            # Simulate image pull via MCP
            pull_result = await self._mcp_call("docker/image/pull", {"image": image})
            if not pull_result.get("success", True):
                return f"MCP Error: Failed to pull image {image}"
            
            # Simulate container creation via MCP
            container_id = f"mock_{uuid.uuid4().hex[:12]}"
            create_result = await self._mcp_call(
                "docker/container/create", 
                {"image": image, "name": name}
            )
            
            # Simulate container start via MCP
            start_result = await self._mcp_call(
                "docker/container/start",
                {"container": container_id}
            )
            
            # Store container info
            self.containers[container_id] = {
                "id": container_id,
                "name": name,
                "image": image,
                "status": "running",
                "created_at": datetime.now().isoformat(),
                "ports": ports or {}
            }
            
            return (
                f"✅ Successfully deployed via Docker MCP Gateway!\n"
                f"• Container ID: {container_id}\n"
                f"• Image: {image}\n"
                f"• Name: {name}\n"
                f"• Status: Running\n"
                f"• Protocol: MCP v{self.mcp_version}\n"
                f"• Ports: {ports or 'None'}"
            )
            
        except Exception as e:
            return f"❌ MCP Deployment Error: {str(e)}"
    
    async def _mcp_call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate MCP protocol call with realistic responses
        """
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Simulate occasional failures (10% chance)
        if random.random() < 0.1:
            return {"success": False, "error": "Simulated MCP gateway timeout"}
        
        # Return successful MCP response
        return {
            "jsonrpc": "2.0",
            "result": {
                "success": True,
                "method": method,
                "timestamp": datetime.now().isoformat()
            },
            "id": str(uuid.uuid4())
        }
    
    async def list_containers(self) -> str:
        """Mock container listing via MCP"""
        if not self.containers:
            return "No containers running via MCP Gateway"
        
        result = "📦 Containers managed by Docker MCP Gateway:\n"
        for container_id, info in self.containers.items():
            result += f"• {info['name']} ({container_id[:12]}) - {info['status']} - {info['image']}\n"
        
        return result
    
    async def get_mcp_status(self) -> str:
        """Get MCP Gateway status"""
        return (
            "🔌 Docker MCP Gateway Status:\n"
            f"• Protocol Version: {self.mcp_version}\n"
            f"• Connected: True\n"
            f"• Active Containers: {len(self.containers)}\n"
            f"• Available Images: {len(self.images)}\n"
            "• Capabilities: container management, image operations, network config"
        )

# Global mock instance
docker_mcp_mock = DockerMCPMockClient()