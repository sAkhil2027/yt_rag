import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb

from config import GOOGLE_API_KEY


_genai_client = None

def get_genai_client():
    global _genai_client
    if _genai_client is None:
        api_key = GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables or .env file.")
        _genai_client = genai.Client(api_key=api_key)
    return _genai_client


def get_gemini_embedding(texts):
    """
    Generates embeddings using Google Gemini embedding models (text-embedding-004 / gemini-embedding-001).
    Accepts either a single string or a list of strings.
    Returns a list of embedding vectors.
    """
    client = get_genai_client()
    is_single = isinstance(texts, str)
    items = [texts] if is_single else texts

    embeddings = []
    # Batch in groups of 30 for safe API throughput
    batch_size = 30
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        try:
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=batch
            )
        except Exception:
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=batch
            )
        for emb in response.embeddings:
            embeddings.append(emb.values)

    return embeddings


def _chromadb_text_to_vector(document: str, video_id: str):
    print(f"Storing embeddings for Video ID: {video_id} (Full transcript length: {len(document)} chars)")

    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if re-ingesting to clear stale chunks
    try:
        client.delete_collection(name=f"{video_id}")
    except Exception:
        pass

    collection = client.get_or_create_collection(name=f"{video_id}")

    try:
        # Optimal RAG chunks: 800 chars with 150 overlap for complete thoughts
        text_split = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = text_split.split_text(document)

        print(f"Generated {len(chunks)} chunks for video_id {video_id}")

        # Generate lightweight embeddings via Google Gemini API
        embadding = get_gemini_embedding(chunks)

        # Generate IDs
        ids = [f"{video_id}_chunk{i}" for i in range(len(chunks))]

        # Metadata
        metadata = [{
            "video_id": video_id,
            "chunk_number": i
        } for i in range(len(chunks))]

        # Store data in ChromaDB
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embadding,
            metadatas=metadata
        )

        return {
            "message": f"[SUCCESS] {len(chunks)} chunks stored successfully using Gemini Embeddings!",
            "video_id": video_id,
            "total_chunks": len(chunks)
        }
    except Exception as e:
        raise Exception(f"error: {e}")
