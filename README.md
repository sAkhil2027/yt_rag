---
title: YT Helper - YouTube AI RAG Chatbot
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

<div align="center">

# 🎬 YT Helper — YouTube AI RAG Chatbot & API

### Ask questions about any YouTube video without watching the entire video.

<p>
  <strong>YouTube URL → Supadata / Invidious Extractor → Semantic Chunker → Google Gemini Embeddings → ChromaDB → Context Retrieval → Groq Cloud LPU Inference</strong>
</p>

<br>

[![Live Backend](https://img.shields.io/badge/Render-Live_Backend-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://video-chatbot-ihi8.onrender.com/)
[![Interactive Swagger](https://img.shields.io/badge/FastAPI-Swagger_Docs-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://video-chatbot-ihi8.onrender.com/docs)
[![Vercel Frontend](https://img.shields.io/badge/Vercel-Live_Frontend-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://ytrag-seven.vercel.app/)
[![FastMCP](https://img.shields.io/badge/FastMCP-AI_Agent_Server-8A2BE2?style=for-the-badge)](mcp_server.py)

<br>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_Cloud-LPU_Inference-F55036?style=flat-square&logo=meta&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F61?style=flat-square)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-Embeddings-4285F4?style=flat-square&logo=google&logoColor=white)
![Supadata](https://img.shields.io/badge/Supadata-Transcript_API-10B981?style=flat-square)

<br>

| Service | Live URL | Status |
| :--- | :--- | :--- |
| **Live Backend API** | [https://video-chatbot-ihi8.onrender.com/](https://video-chatbot-ihi8.onrender.com/) | Active |
| **Interactive Swagger Docs** | [https://video-chatbot-ihi8.onrender.com/docs](https://video-chatbot-ihi8.onrender.com/docs) | Active |
| **Health Check Endpoint** | [https://video-chatbot-ihi8.onrender.com/health](https://video-chatbot-ihi8.onrender.com/health) | Active |
| **Live Web Frontend (Vercel)** | [https://ytrag-seven.vercel.app/](https://ytrag-seven.vercel.app/) | Connected |

</div>

---

## ✨ Overview

**YT Helper** is a high-performance Retrieval-Augmented Generation (RAG) system, REST API, and interactive glassmorphic web application that allows users and autonomous AI agents to query, summarize, and extract insights from any YouTube video in real time.

By extracting transcripts through a resilient multi-tier pipeline (**Supadata API** $\rightarrow$ **YouTubeTranscriptApi** $\rightarrow$ **Invidious Mirrors** $\rightarrow$ **Direct Paste Fallback**), vectorizing text into **ChromaDB** using **Google Gemini Embeddings**, and performing streaming inference via **Groq Cloud LPU**, YT Helper generates grounded, factual answers in seconds with minimal token consumption.

```text
🎥 YouTube Video URL / Text
       │
       ▼
📝 Multi-Tier Extraction Engine
   ├── Tier 1: Supadata Transcript API (100% cloud bypass)
   ├── Tier 2: YouTubeTranscriptApi (en, hi, es, fr, de)
   ├── Tier 3: Decentralized Invidious Mirrors
   └── Tier 4: Manual Direct Paste UI (/ingest_transcript)
       │
       ▼
✂️ Semantic Chunker (RecursiveCharacterTextSplitter: 800 chars / 150 overlap)
       │
       ▼
🧠 Dense Vector Embeddings (Google Gemini text-embedding-004 / gemini-embedding-001)
       │
       ▼
🗄️ Persistent ChromaDB Vector Database (Named collections per Video ID)
       │
       ▼
🔎 Cosine Similarity Search (Top 5 Chunks / ~4,000 chars context)
       │
       ▼
⚡ Groq Cloud LPU Inference Engine (Qwen 3.8 27B / GPT-OSS 120B / Llama 3.3)
       │
       ▼
💬 Real-Time Token Streaming (Web UI & FastMCP Protocol for AI Agents)
```

---

## 🚀 Key Features

- **🛡️ Anti-Block Transcript Pipeline**: Combines Supadata API, local extraction, public mirrors, and manual transcript pasting to eliminate datacenter IP blocks on Render/AWS.
- **⚡ Ultra-Fast Groq Cloud Inference**: Delivers streaming token generation powered by active verified models (`qwen/qwen3.8-27b`, `openai/gpt-oss-120b`, `llama-3.3-70b-versatile`) with automatic quota failover.
- **📉 Optimized Token Economics**: Responses are strictly capped to ~300 tokens (`max_tokens=300`) with top-5 chunk retrieval, cutting prompt token overhead by 35% and keeping costs under ~$0.001 per query.
- **🧠 Google Gemini Dense Vectors**: Uses official Google GenAI SDK (`text-embedding-004` / `gemini-embedding-001`) with task-specific optimization (`RETRIEVAL_DOCUMENT` vs `RETRIEVAL_QUERY`).
- **🗄️ ChromaDB Local Vector Store**: Persists document vectors into named SQLite collections per video (`vid_{video_id}`).
- **🖥️ Dark Glassmorphic Web UI**: Vanilla CSS single-page interface with real-time SSE token streaming, suggestion chips, live connection status indicators, and one-click copy buttons.
- **🔌 Model Context Protocol (MCP)**: Native FastMCP server implementation (`mcp_server.py`) for AI agents in Cursor, Claude Desktop, and Antigravity.
- **💓 Built-in Free-Tier Keep-Alive**: Background asynchronous heartbeat worker pings `/health` every 12 minutes if `RENDER_EXTERNAL_URL` is set, preventing Render instances from sleeping.

---

## 🏗️ Project Architecture & File Structure

```text
Tube-AI-API/
├── app.py                     # FastAPI REST API, streaming endpoints, and keep-alive worker
├── mcp_server.py              # FastMCP server exposing ingest & query tools for AI IDEs
├── config.py                  # Environment variable configuration loader
├── requirements.txt           # Python dependency specifications
├── render.yaml                # Render Blueprint infrastructure-as-code specification
├── vercel.json                # Vercel root routing and rewrite rules
├── Dockerfile                 # Multi-cloud container manifest (Hugging Face / Cloud Run)
├── DEPLOYMENT.md              # Detailed step-by-step production deployment guide
├── token_calculation.md       # In-depth mathematical token and cost analysis
├── README.md                  # Comprehensive project documentation
├── .env.example               # Template environment variables
├── .gitignore                 # Exclusion rules for secrets, DBs, and virtualenvs
│
├── services/                  # Backend RAG Core Services
│   ├── __init__.py
│   ├── chunk_extractor.py     # Multi-tier YouTube extraction (Supadata + Invidious + local)
│   ├── embadding.py           # LangChain text splitter, Gemini embeddings & ChromaDB storage
│   ├── query.py               # Vector similarity search engine (top 5 chunks)
│   ├── groq_connection.py     # Groq API streaming inference, model rotation & token cap
│   └── ollama_connection.py   # Local offline Ollama backup connection
│
├── frontend/                  # Standalone Vercel-Ready Frontend
│   ├── index.html             # Responsive dark-mode Chatbot UI (streaming text reader)
│   ├── config.js              # Production API backend URL configuration
│   └── vercel.json            # Vercel rewrite configuration
│
└── static/                    # Embedded Static UI for FastAPI
    ├── index.html             # Exact mirror of frontend/index.html served at GET /
    └── config.js              # Mirrored backend configuration
```

---

## 📡 API Endpoints Reference

### 1. Ingest YouTube Video by URL
Extracts transcript, chunks text, generates embeddings, and saves into ChromaDB.

* **URL**: `POST /youtube_url`
* **Headers**: `Content-Type: application/json`
* **Body**:
  ```json
  {
    "url": "https://www.youtube.com/watch?v=VNaj4yhqtQg"
  }
  ```
* **Response (`200 OK`)**:
  ```json
  {
    "message": "[SUCCESS] 13 chunks stored successfully using Gemini Embeddings!",
    "video_id": "VNaj4yhqtQg",
    "total_chunks": 13
  }
  ```

---

### 2. Ask Question (Real-Time Streaming)
Streams answer tokens incrementally using Server-Sent text/plain streaming.

* **URL**: `POST /query_stream`
* **Headers**: `Content-Type: application/json`
* **Body**:
  ```json
  {
    "query": "What are the main key takeaways from this video?",
    "video_id": "VNaj4yhqtQg"
  }
  ```
* **Response**: Real-time token-by-token stream.

---

### 3. Ask Question (Synchronous Non-Streaming)
* **URL**: `POST /query`
* **Headers**: `Content-Type: application/json`
* **Body**:
  ```json
  {
    "query": "Summarize the conclusion of this video.",
    "video_id": "VNaj4yhqtQg"
  }
  ```
* **Response (`200 OK`)**:
  ```json
  {
    "message": "The video concludes by emphasizing..."
  }
  ```

---

### 4. Direct Transcript Ingestion (Bypass Fallback)
Ingests raw transcript text directly, bypassing YouTube network requests entirely.

* **URL**: `POST /ingest_transcript`
* **Headers**: `Content-Type: application/json`
* **Body**:
  ```json
  {
    "video_id": "VNaj4yhqtQg",
    "text": "Full copied transcript text goes here..."
  }
  ```

---

### 5. Health Check Endpoint
* **URL**: `GET /health`
* **Response (`200 OK`)**:
  ```json
  {
    "status": "healthy",
    "service": "YT Helper"
  }
  ```

---

## 🛠️ Local Installation & Development

### 1. Clone the Repository
```bash
git clone https://github.com/sAkhil2027/yt_rag.git
cd yt_rag
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```env
# Required for Groq Cloud inference
GROQ_API_KEY=your_groq_api_key_here

# Required for Google Gemini embeddings
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Supadata Transcript API (recommended for cloud servers)
SUPADATA_API_KEY=your_supadata_api_key_here
```

### 5. Run the Local Server
```bash
python -m uvicorn app:app --reload --port 7860
```
Open **`http://localhost:7860`** in your browser to start chatting!

---

## 🔌 Model Context Protocol (MCP) Server

YT Helper includes a built-in **FastMCP** server to let AI assistants (Cursor, Claude Desktop, Antigravity) ingest and query YouTube videos directly inside coding environments.

### Run MCP Server:
```bash
python mcp_server.py
```

### Claude Desktop Configuration:
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "yt-helper": {
      "command": "python",
      "args": ["f:/path-to-repo/mcp_server.py"]
    }
  }
}
```

---

## 🚀 Cloud Deployment

For a detailed step-by-step guide, check out **[DEPLOYMENT.md](DEPLOYMENT.md)**.

* **Backend on Render**: Deploys automatically via `render.yaml` with auto keep-alive.
* **Frontend on Vercel**: Connects directly to `https://video-chatbot-ihi8.onrender.com/` without requiring visitor configuration.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
