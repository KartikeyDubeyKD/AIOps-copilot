# ⚡ AI Ops Copilot

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](https://ai-ops-copilot.vercel.app/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-blue)](https://aiops-copilot.onrender.com)
[![Frontend](https://img.shields.io/badge/Frontend-React-purple)](https://ai-ops-copilot.vercel.app/)

> **AI Ops Copilot** is an intelligent DevOps assistant that turns natural language into real infrastructure actions using **Cerebras Cloud**, **Meta Llama**, and the **Docker MCP Gateway**.  
> Chat with your infrastructure — analyze logs, get AI-driven recommendations, and trigger deployments seamlessly.

---

## 🏆 Hackathon Sponsor Integrations

| Sponsor | Integration | Status |
|----------|--------------|---------|
| **Cerebras** | Real-time log analysis using Cerebras Cloud API | ✅ Implemented |
| **Meta AI** | AI recommendations using Llama 3.1 8B via Hugging Face Inference API | ✅ Implemented |
| **Docker** | Container deployments via the MCP Gateway pattern | ✅ Implemented |

---

## 🚀 Key Features

- **🤖 Conversational AI Interface** – Chat naturally with your DevOps assistant  
- **📊 Log Analysis** – Upload `.log` or `.txt` files for instant AI-generated summaries (Cerebras)  
- **🛠️ Troubleshooting Assistant** – Actionable remediation steps via Meta Llama  
- **🐳 Smart Deployments** – Trigger service deployments using Docker MCP Gateway  
- **💬 Context Awareness** – Conversation memory across multiple queries  

---

## 🧱 Architecture

```text
┌────────────────────────┐      ┌─────────────────────────┐      ┌───────────────────────────┐
│        React UI        │─────▶│        FastAPI          │─────▶│        AI Services        │
│  • Chat / Upload Logs  │      │  • REST / Chat API      │      │  • Cerebras Cloud API     │
│  • Natural Commands    │      │  • Context & Routing     │      │  • Meta Llama 3 8B (HF)   │
└────────────────────────┘      │  • Docker MCP Gateway    │      └───────────────────────────┘
                                └────────────┬─────────────┘
                                             │
                                     ┌───────▼────────┐
                                     │   Docker Host   │
                                     │  (Deployments)  │
                                     └─────────────────┘
```

🛠️ Tech Stack
**Backend**

  🧩 FastAPI · Uvicorn
  
  🤖 Cerebras Cloud SDK
  
  🧠 Hugging Face Inference API (Llama 3.1 8B Instruct)
  
  🐳 Docker MCP Gateway (Mock for Demo)
  
  🔐 Pydantic for validation

**Frontend**
  
  ⚛️ React (via Vite)
  
  💨 Tailwind CSS
  
  🌐 Axios for API calls
  
  📝 React Markdown for rich responses

⚙️ Setup Guide
**Prerequisites**
```text
Python 3.8 +

Node.js 16 +

Docker Engine (optional for deploy testing)
```
Backend Setup
git clone https://github.com/<your-username>/ai-ops-copilot
cd ai-ops-copilot/backend

## 1️⃣ Install dependencies
```
pip install -r requirements.txt
```

## 2️⃣ Create environment file
```
cp .env.example .env
```

## Add your keys:
### CEREBRAS_API_KEY=your_cerebras_key
### HF_API_TOKEN=your_huggingface_token


## 3️⃣ Run the server
```
uvicorn main:app --reload --port 8000
```

Backend will start at http://127.0.0.1:8000

Swagger Docs → http://127.0.0.1:8000/docs

# Frontend Setup
cd ../frontend

## 1️⃣ Install dependencies
npm install

## 2️⃣ Set environment variable
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env

## 3️⃣ Run the frontend
npm run dev


Frontend runs at http://127.0.0.1:5173

☁️ Deployment
Backend (Render)

Auto-deployed from main branch.

Environment variables are configured in the Render Dashboard.

Live API → https://aiops-copilot.onrender.com

Frontend (Vercel)

Connected to GitHub repo.

Uses .env.production for the deployed API URL.

Live App → https://ai-ops-copilot.vercel.app

🔐 Environment Variables
Key	Description
CEREBRAS_API_KEY	API key from Cerebras Cloud
HF_API_TOKEN	Hugging Face API token (for Llama)
VITE_API_BASE_URL	Backend base URL (frontend env)
💡 How It Works

Upload Logs or Type Command

/analyze-logs-upload → Cerebras analyzes logs in real-time.

AI Recommends Fixes

/recommend-actions or /copilot-chat → Llama suggests solutions.

Trigger Deployments

/deploy → Docker MCP Gateway deploys the service.

Conversational Context

/copilot-chat preserves chat history for context-aware answers.


🧩 Environment Switching

You can easily switch between local and deployed backends:
.env
VITE_API_BASE_URL=http://127.0.0.1:8000

.env.production
VITE_API_BASE_URL=https://aiops-copilot.onrender.com

Vite automatically picks the correct one during build.

📽️ Demo Preview

Live Demo: https://ai-ops-copilot.vercel.app
Backend API: https://aiops-copilot.onrender.com/docs

🤝 Contributing
# 1. Fork the repo
# 2. Create a branch
```
git checkout -b feature/awesome-feature
```
# 3. Commit your changes
```
git commit -m "Add awesome feature"
```
# 4. Push and open a PR
```
git push origin feature/awesome-feature
```
