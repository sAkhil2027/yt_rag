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
