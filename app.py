import os
import asyncio
import urllib.request
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.query import user_query
from services.groq_connection import groq_model, groq_model_stream
from services.chunk_extractor import chunk_extractor
from services.embadding import _chromadb_text_to_vector


# Request data structures
class userURL(BaseModel):
    url: str

class userTranscript(BaseModel):
    video_id: str
    text: str

class userQuery(BaseModel):
    query: str
    video_id: str


async def render_keep_alive():
    """
    Background worker that pings this service every 12 minutes if deployed on Render.
    Prevents Render free tier from sleeping after 15 minutes of inactivity.
    """
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if not render_url:
        return

    health_url = f"{render_url.rstrip('/')}/health"
    print(f"[INIT] Render keep-alive self-heartbeat enabled targeting: {health_url}")

    while True:
        await asyncio.sleep(720)  # 12 minutes
        try:
            req = urllib.request.Request(health_url, headers={"User-Agent": "Render-KeepAlive/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[HEARTBEAT] Keep-alive ping successful: status {resp.status}")
        except Exception as e:
            print(f"[WARN] Keep-alive self-ping encountered error: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    heartbeat_task = asyncio.create_task(render_keep_alive())
    yield
    heartbeat_task.cancel()


app = FastAPI(
    title="YT Helper API",
    description="""
    YT Helper RAG API and AI Chatbot for YouTube Videos. Ask questions about any YouTube video without watching the full video.
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for external frontends (e.g. Vercel), mobile clients, and cross-origin requests
cors_origins_raw = os.getenv("CORS_ORIGINS", "*")
if cors_origins_raw.strip() == "*":
    cors_origins = ["*"]
else:
    cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Mount static/frontend UI folder
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    static_dir = os.path.join(os.path.dirname(__file__), "frontend")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/health")
async def health_check():
    """Lightweight health check endpoint for monitoring and Render keep-alive pings."""
    return {"status": "healthy", "service": "YT Helper"}


@app.get("/")
async def home():
    """Serves the interactive YT Helper Chatbot UI with caching disabled for instant updates."""
    html_path = os.path.join(static_dir, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Welcome to YT Helper API"}


@app.get("/config.js")
async def get_config():
    """Serves config.js directly so relative script paths load without 404."""
    cfg_path = os.path.join(static_dir, "config.js")
    if not os.path.exists(cfg_path):
        cfg_path = os.path.join(os.path.dirname(__file__), "frontend", "config.js")
    if os.path.exists(cfg_path):
        return FileResponse(cfg_path, media_type="application/javascript", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "config.js not found"}


@app.post("/youtube_url")
@app.post("/yourube_url")
async def text_extractor(data: userURL):
    try:
        result = chunk_extractor(data.url)
        res = _chromadb_text_to_vector(result["text"], result["video_id"])
        return res
    except Exception as e:
        return {"message": str(e)}


@app.post("/ingest_transcript")
async def ingest_direct_transcript(data: userTranscript):
    """Direct transcript ingestion endpoint allowing client-side residential fallback."""
    try:
        res = _chromadb_text_to_vector(data.text, data.video_id)
        return res
    except Exception as e:
        return {"message": str(e)}


@app.post("/query")
async def ask_query(query: userQuery):
    try:
        result = user_query(query.query, query.video_id)
        ai_response = groq_model(query.query, result[0])
        return {"message": str(ai_response)}
    except Exception as e:
        return {"message": str(e)}


@app.post("/query_stream")
async def ask_query_stream(query: userQuery):
    try:
        result = user_query(query.query, query.video_id)
        return StreamingResponse(
            groq_model_stream(query.query, result[0]),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    except Exception as e:
        return StreamingResponse(
            iter([f"Error: {e}"]),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"}
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
