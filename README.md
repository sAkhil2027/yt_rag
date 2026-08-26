<div align="center">

# 🎬 YT Helper — YouTube AI RAG Chatbot & API

### Ask questions about any YouTube video without watching the entire video.

<p>
  <strong>YouTube URL → Transcript Extraction → 800-Char Chunking → SentenceTransformers → ChromaDB → Context Retrieval → Groq Llama 3.3 70B</strong>
</p>

<br>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_Cloud-Llama_3.3_70B-F55036?style=for-the-badge&logo=meta&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F61?style=for-the-badge)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-all--MiniLM--L6--v2-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![MCP](https://img.shields.io/badge/FastMCP-AI_Agent_Server-8A2BE2?style=for-the-badge)

<br>

![GitHub repo size](https://img.shields.io/github/repo-size/sAkhil2027/yt_video-rag-chatbot?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/sAkhil2027/yt_video-rag-chatbot?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/sAkhil2027/yt_video-rag-chatbot?style=flat-square)
![GitHub license](https://img.shields.io/github/license/sAkhil2027/yt_video-rag-chatbot?style=flat-square)

</div>

---

## ✨ Overview

**YT Helper** is a high-performance Retrieval-Augmented Generation (RAG) system and interactive web application that enables users to chat with any YouTube video. 

By extracting 100% of available spoken transcript text, vectorizing it into a local **ChromaDB** database using **SentenceTransformers**, and querying **Groq Cloud's Llama 3.3 70B** model, YT Helper provides instant, grounded answers with timestamps and topic breakdowns in seconds.

```text
🎥 YouTube Video URL
       │
       ▼
📝 Multi-Language Transcript Extractor (YouTubeTranscriptApi)
       │
       ▼
✂️ Semantic Chunker (800 chars / 150 overlap)
       │
       ▼
🧠 Dense Vector Embeddings (all-MiniLM-L6-v2)
       │
       ▼
🗄️ Persistent ChromaDB Vector Store
       │
       ▼
🔎 Cosine Similarity Search (Top 7 Chunks / 5,600 chars)
       │
       ▼
⚡ Groq Cloud LPU Inference Engine (Llama 3.3 70B)
       │
       ▼
💬 Production Dark Glassmorphic Web UI & FastMCP Server
```

---

## 🚀 Key Features

| Feature | Technology / Implementation | Description |
| :--- | :--- | :--- |
| **🎥 Full Transcript Ingestion** | `YouTubeTranscriptApi` | Downloads 100% of spoken transcript text across manual and auto-generated tracks (`en`, `hi`, `es`, `fr`, `de`). |
| **✂️ Optimal RAG Chunking** | `RecursiveCharacterTextSplitter` | Splits long transcripts into 800-character semantic chunks with 150-character overlap to preserve sentence context. |
| **🧠 Local Dense Embeddings** | `all-MiniLM-L6-v2` | Generates 384-dimensional dense vectors locally using SentenceTransformers. |
| **🗄️ Persistent Vector Store** | `ChromaDB` | Stores indexed vector chunks locally under named collections per YouTube video ID. |
| **🔎 Rich Context Retrieval** | Cosine Similarity Search | Retrieves the top **7 most relevant chunks (~5,600 characters)** matching user questions. |
| **⚡ High-Speed LLM Inference** | `Groq Cloud API` | Powered by Groq's ultra-fast LPU engine running **`llama-3.3-70b-versatile`**. |
| **🖥️ Interactive Chatbot UI** | HTML5 / Vanilla CSS / JS | Built-in dark glassmorphic web interface with prompt suggestion cards, syntax highlighting, and copy tools. |
| **🔌 FastMCP Server Integration** | `FastMCP` Protocol | Exposes `ingest_youtube_video` and `query_youtube_video` tools for AI agents (Claude Desktop, Cursor, Antigravity). |

---

## 🏗️ Project Architecture

```text
Tube-AI-API/
├── app.py                     # Main FastAPI server & REST API endpoints
├── mcp_server.py              # FastMCP server for AI agent integrations
├── config.py                  # Environment variable configuration loader
├── requirements.txt           # Python dependencies manifest
├── README.md                  # Complete project documentation
├── .gitignore                 # Git security and exclusion rules
│
├── services/                  # Backend RAG Core Pipeline Services
│   ├── __init__.py
│   ├── chunk_extractor.py     # YouTube transcript extraction service
│   ├── embadding.py           # Text splitter & ChromaDB vector manager
│   ├── query.py               # Vector similarity search engine
│   └── groq_connection.py     # Groq Cloud API LLM service
│
└── static/                    # Frontend User Interface
    └── index.html             # Responsive dark-mode Chatbot UI
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* Python **3.11** or higher
* Git

### 2. Clone the Repository
```bash
git clone https://github.com/sAkhil2027/yt_video-rag-chatbot.git
cd yt_video-rag-chatbot
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```
> *(Get your free high-speed API key at [Groq Console](https://console.groq.com/))*

---

## 🏃 Running the Application

### Option 1: Web Application Server (Recommended)
Run the FastAPI application server:
```bash
python app.py
```
Or using uvicorn reload mode:
```bash
python -m uvicorn app:app --reload
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`**

---

### Option 2: Model Context Protocol (MCP) Server
To connect YT Helper directly to **Claude Desktop**, **Cursor**, or **Antigravity**:

```bash
python mcp_server.py
```

Test interactively via MCP Inspector:
```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

---

## 📡 API Endpoints Reference

### 1. Ingest YouTube Video
* **Endpoint**: `POST /youtube_url`
* **Request Body**:
  ```json
  {
    "url": "https://www.youtube.com/watch?v=A8s-KxHUi3I"
  }
  ```
* **Response**:
  ```json
  {
    "message": "[SUCCESS] 9 chunks stored successfully across complete video transcript!",
    "video_id": "A8s-KxHUi3I",
    "total_chunks": 9
  }
  ```

---

### 2. Ask Question About Video
* **Endpoint**: `POST /query`
* **Request Body**:
  ```json
  {
    "query": "What are the main actionable takeaways from this video?",
    "video_id": "A8s-KxHUi3I"
  }
  ```
* **Response**:
  ```json
  {
    "message": "Based on the video transcript, here are the key takeaways:\n\n1. **Core Concept**: ..."
  }
  ```

---

### 3. Interactive Web UI
* **Endpoint**: `GET /`
* Returns the interactive single-page Chatbot frontend (`static/index.html`).

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the Repository.
2. Create a Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'feat: Add AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
