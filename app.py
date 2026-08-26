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

