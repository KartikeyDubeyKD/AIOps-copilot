# AI Ops Copilot 🚀
An AI-powered DevOps assistant built with **FastAPI**, **Meta Llama**, **Cerebras**, and **Docker MCP Gateway**.

## Problem
Managing cloud-native infrastructure is complex, requiring constant monitoring, debugging, and container orchestration.

## Solution
AI Ops Copilot turns natural language into real DevOps actions:
- **Deploy containers** with Docker MCP Gateway
- **Analyze logs** with Cerebras Cloud + Llama
- **Explain issues** in plain English

## Tech Stack
- Backend: FastAPI (Python)
- AI: Meta Llama, Cerebras Cloud
- Infra: Docker MCP Gateway
- Frontend: React (coming soon)

## Setup (Backend)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

### Deploy Example
Request:
```bash
POST /deploy
{ "service_name": "redis", "image": "redis:latest" }