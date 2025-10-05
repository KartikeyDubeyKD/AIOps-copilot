# ⚡ AI Ops Copilot

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](https://your-vercel-app.vercel.app)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-blue)](https://your-backend.onrender.com)
[![Frontend](https://img.shields.io/badge/Frontend-React-purple)](https://your-vercel-app.vercel.app)

> An intelligent DevOps assistant that turns natural language into real infrastructure actions using **Cerebras**, **Meta Llama**, and **Docker MCP Gateway**.

## 🏆 Hackathon Sponsor Integrations

| Sponsor | Integration | Status |
|---------|-------------|---------|
| **Cerebras** | Real-time log analysis using Cerebras Cloud API | ✅ **Implemented** |
| **Meta** | AI recommendations using Llama-3.1-8B via HuggingFace | ✅ **Implemented** |
| **Docker** | Container deployment using MCP Gateway pattern | ✅ **Implemented** |

## 🚀 Features

- **🤖 Intelligent Chat Interface** - Natural language conversations about your infrastructure
- **📊 Log Analysis** - Upload log files and get AI-powered insights using Cerebras
- **🛠️ Troubleshooting** - Get actionable recommendations using Meta Llama
- **🐳 Container Deployment** - Deploy services using Docker MCP Gateway
- **💬 Context-Aware** - Remembers conversation history and previous analyses

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Cerebras Cloud SDK** - AI-powered log analysis
- **HuggingFace Inference API** - Meta Llama integration
- **Docker MCP Gateway** - Container orchestration
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React** - Modern UI framework
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **React Markdown** - Rich text rendering
- **Tailwind CSS** - Styling

## 📦 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker Engine (for local deployments)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/ai-ops-copilot
cd ai-ops-copilot/backend

### Install dependencies
```bash
pip install -r requirements.txt

### Set up environment variables
```
cp .env.example .env
# Add your API keys:
# CEREBRAS_API_KEY=your_cerebras_key
# HF_API_TOKEN=your_huggingface_token


### Run the backend
```bash
uvicorn main:app --reload --port 8000

###Frontend Setup
Navigate to frontend directory
```bash
cd ../frontend

### Install dependencies
```bash
npm install

### Run the frontend
Run the frontend
```bash
Run the frontend


###Architecture
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React         │    │   FastAPI        │    │   AI Services   │
│   Frontend      │────│   Backend        │────│                 │
│                 │    │                  │    │  • Cerebras     │
│ • Chat UI       │    │ • REST API       │    │  • Meta Llama   │
│ • File Upload   │    │ • Auth & CORS    │    └─────────────────┘
└─────────────────┘    │ • Docker MCP     │
                       └──────────────────┘
                                │
                        ┌───────┴───────┐
                        │   Docker      │
                        │   Engine      │
                        └───────────────┘


## 🚀 Deployment

###Backend (Render)
```bash
# Deployed automatically from main branch
# Environment variables set in Render dashboard

###Fronten (Vercel)
```bash
# Connected to GitHub repo
# Automatic deployments on push



###🤝 Contributing
```bash 
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

