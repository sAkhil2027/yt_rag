import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import IO, Any, Literal

from services.query import user_query
from services.groq_connection import groq_model
from services.chunk_extractor import chunk_extractor
from services.embadding import _chromadb_text_to_vector

# Request structure
class userURL(BaseModel):
    url: str

class userQuery(BaseModel):
    query: str
    video_id: str

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="YT Helper API",
    description="""
    YT Helper RAG API and AI Chatbot for YouTube Videos. Ask questions about any YouTube video without watching the full video.
    """,
    version="1.0.0"
)

