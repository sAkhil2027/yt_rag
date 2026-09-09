# 🚀 Deployment Guide: Backend on Render & Frontend on Vercel

This guide provides step-by-step instructions for deploying **YT Helper** with the **FastAPI Backend on Render** and the **Web Frontend on Vercel**.

---

## 🏗️ Architecture Overview

```text
┌───────────────────────────────────────┐
│           Vercel Frontend             │
│   (https://your-frontend.vercel.app)  │
│                                       │
│   • HTML5 / Vanilla CSS / JS UI       │
│   • Real-Time Token Streaming Reader  │
│   • Browser Fallback Mirror Scraper   │
└──────────────────┬────────────────────┘
                   │
                   │ Cross-Origin HTTPS Requests
                   │ (CORS Enabled)
                   ▼
┌───────────────────────────────────────┐
│            Render Backend             │
│   (https://your-service.onrender.com) │
│                                       │
│   • FastAPI REST + Streaming API      │
│   • LangChain Chunking Engine         │
│   • Google Gemini Embeddings          │
│   • ChromaDB Vector Store             │
│   • Groq Cloud LLM Inference Engine   │
│   • Auto Keep-Alive Self-Heartbeat    │
└───────────────────────────────────────┘
```

---

## Part 1: Deploy Backend on Render

### Step 1: Create a Render Web Service
1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** → **Web Service**.
3. Connect your GitHub repository (`yt_video-rag-chatbot` / `Tube-AI-API`).
4. Configure the service settings:
   - **Name**: `yt-helper-api` (or your preferred name)
   - **Root Directory**: Leave blank / empty (since `app.py` is at the root of the repository)
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn app:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: `Free`

*(Alternatively, if you use Render Blueprints, Render will automatically detect the provided [`render.yaml`](render.yaml) file!)*

---

### Step 2: Configure Environment Variables
In the **Environment** tab of your Render service, add the following variables:

| Variable | Required | Value / Description |
| :--- | :---: | :--- |
| `GROQ_API_KEY` | **Yes** | Your Groq Cloud API key ([console.groq.com](https://console.groq.com/)) |
| `GOOGLE_API_KEY` | **Yes** | Your Google Gemini API key ([aistudio.google.com](https://aistudio.google.com/)) |
| `RENDER_EXTERNAL_URL` | **Recommended** | Your Render service URL: `https://yt-helper-api.onrender.com`<br>*(Enables built-in background ping to prevent free-tier sleeping)* |
| `CORS_ORIGINS` | Optional | `*` (default) or your Vercel URL (e.g. `https://your-app.vercel.app`) |
| `PYTHON_VERSION` | Optional | `3.11.9` |

---

### Step 3: Deploy & Verify
1. Click **Deploy Web Service**.
2. Once deployed, test the health check in your browser:
   ```text
   https://your-service.onrender.com/health
   ```
   You should see:
   ```json
   {"status":"healthy","service":"YT Helper"}
   ```
3. Copy your Render URL (e.g. `https://your-service.onrender.com`). You will need this for the frontend!

---

## Part 2: Deploy Frontend on Vercel

### Step 1: Import Project to Vercel
1. Go to your [Vercel Dashboard](https://vercel.com/new).
2. Click **"Add New..."** → **"Project"**.
3. Import your GitHub repository.

---

### Step 2: Configure Vercel Project Settings
1. In the **Configure Project** screen:
   - **Framework Preset**: Select **Other** (leave Build Command and Output Directory blank).
   - **Root Directory**: Select **`frontend`** (or leave as repository root — the included root `vercel.json` will automatically route to `/frontend`!).
2. Click **Deploy**!

---

## Part 3: Connecting Frontend to Backend

You have two easy options to connect the frontend to your Render backend:

### Option A: In-App UI Configuration (Easiest, No Rebuild)
1. Open your newly deployed Vercel URL (e.g. `https://your-frontend.vercel.app`).
2. Click the **"API Config"** button in the topbar.
3. Paste your Render URL: `https://your-service.onrender.com`.
4. Click **"Ping / Health Check"** to confirm the connection.
5. Click **"Save & Connect"**. The frontend saves this in `localStorage` and connects immediately!

### Option B: Set Default in `config.js` (Before Deploying)
In [`frontend/config.js`](frontend/config.js), set your Render URL:
```javascript
window.CONFIG = {
  API_BASE_URL: "https://your-service.onrender.com"
};
```
Commit and push to GitHub. Vercel will automatically redeploy with the configured backend URL.

---

## ⚡ Key Production Tips

1. **Free Tier Cold Starts**:
   - Render's free tier spins down instances after 15 minutes of inactivity.
   - The first request after sleep may take ~50 seconds while the instance wakes up.
   - Setting `RENDER_EXTERNAL_URL` in your Render Environment Variables enables the built-in 12-minute keep-alive ping to keep the service warm during active hours.

2. **ChromaDB Storage on Free Tier**:
   - Render free tier instances have ephemeral storage. Embeddings are stored in `./chroma_db` during the active session. If the container restarts, ingest the video URL again.
   - If you require persistent storage across restarts, attach a Render Persistent Disk and set `CHROMA_PERSIST_DIR=/var/data/chroma_db`.

3. **Datacenter YouTube Blocking**:
   - If YouTube blocks Render's IP address when fetching transcripts, the frontend automatically falls back to decentralized Invidious mirrors and client-side browser scraping via `/ingest_transcript`.
