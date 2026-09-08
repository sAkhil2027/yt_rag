import sys
import os

# Ensure current directory is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from services.chunk_extractor import chunk_extractor
from services.embadding import _chromadb_text_to_vector
from services.query import user_query
from services.groq_connection import groq_model

# Initialize FastMCP Server for YT Helper
mcp = FastMCP("YT Helper")

@mcp.tool()
def ingest_youtube_video(url: str) -> str:
    """
    Ingest a YouTube video transcript into ChromaDB vector database for RAG queries.
    Args:
        url: Valid YouTube video URL or video ID.
    """
    try:
        extracted = chunk_extractor(url)
        video_id = extracted["video_id"]
        res = _chromadb_text_to_vector(extracted["text"], video_id)
        return f"✅ Successfully ingested YouTube video ID '{video_id}'. {res.get('message', '')}"
    except Exception as e:
        return f"❌ Error ingesting YouTube video: {e}"

@mcp.tool()
def query_youtube_video(query: str, video_id: str) -> str:
    """
    Query an ingested YouTube video using RAG and Groq AI.
    Args:
        query: Question about the YouTube video.
        video_id: 11-character YouTube video ID.
    """
    try:
        context = user_query(query, video_id)
        if not context or not context[0]:
            return f"⚠️ No transcript context found for video ID '{video_id}'. Please call ingest_youtube_video first."
        answer = groq_model(query, context[0])
        return str(answer)
    except Exception as e:
        return f"❌ Error querying video '{video_id}': {e}"

if __name__ == "__main__":
    mcp.run()
