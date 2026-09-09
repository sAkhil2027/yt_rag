import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.query import user_query
from services.groq_connection import groq_model, groq_model_stream
from services.chunk_extractor import chunk_extractor
from services.embadding import _chromadb_text_to_vector

class userURL(BaseModel):
    url: str

class userQuery(BaseModel):
    query: str
    video_id: str

app = FastAPI(title="YT Helper API", version="1.0.0")

cors_origins_raw = os.getenv("CORS_ORIGINS", "*")
cors_origins = ["*"] if cors_origins_raw.strip() == "*" else [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def home():
    html_path = os.path.join(static_dir, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Welcome to YT Helper API"}

@app.post("/youtube_url")
async def text_extractor(data: userURL):
    result = chunk_extractor(data.url)
    return _chromadb_text_to_vector(result["text"], result["video_id"])

@app.post("/query")
async def ask_query(query: userQuery):
    result = user_query(query.query, query.video_id)
    return {"message": str(groq_model(query.query, result[0]))}

@app.post("/query_stream")
async def ask_query_stream(query: userQuery):
    result = user_query(query.query, query.video_id)
    return StreamingResponse(groq_model_stream(query.query, result[0]), media_type="text/plain")
