import os
from typing import List, Union
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from google.genai import types
import chromadb

from config import GOOGLE_API_KEY

_genai_client = None

def get_genai_client() -> genai.Client:
    global _genai_client
    if _genai_client is None:
        api_key = GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables or .env file.")
        _genai_client = genai.Client(api_key=api_key)
    return _genai_client

def get_gemini_embedding(
    texts: Union[str, List[str]], 
    task_type: str = "RETRIEVAL_DOCUMENT",
    **kwargs
) -> List[List[float]]:
    client = get_genai_client()
    items = [texts] if isinstance(texts, str) else texts
    embeddings = []
    batch_size = 30
    config = types.EmbedContentConfig(task_type=task_type)
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        try:
            response = client.models.embed_content(model="gemini-embedding-001", contents=batch, config=config)
        except Exception:
            response = client.models.embed_content(model="text-embedding-004", contents=batch, config=config)
        for emb in response.embeddings:
            embeddings.append(emb.values)
    return embeddings

def _chromadb_text_to_vector(document: str, video_id: str):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name=f"{video_id}")
    text_split = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = text_split.split_text(document)
    embeddings = get_gemini_embedding(chunks)
    ids = [f"{video_id}_chunk{i}" for i in range(len(chunks))]
    metadata = [{"video_id": video_id, "chunk_number": i} for i in range(len(chunks))]
    collection.add(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadata)
    return {"message": f"[SUCCESS] {len(chunks)} chunks stored successfully!", "video_id": video_id, "total_chunks": len(chunks)}
