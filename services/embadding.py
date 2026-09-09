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
    """
    Generates embeddings using Google Gemini embedding models with task_type optimization.
    Accepts a single string or a list of strings and returns a list of embedding vectors.
    """
    task_type = kwargs.get("task_type", task_type)
    client = get_genai_client()
    items = [texts] if isinstance(texts, str) else texts

    embeddings = []
    batch_size = 30
    
    # Configure task type for optimal semantic search vector representation
    config = types.EmbedContentConfig(task_type=task_type)

    candidate_models = ["gemini-embedding-001", "text-embedding-004", "gemini-embedding-exp-03-07", "gemini-embedding-2"]

    for i in range(0, len(items), batch_size):
        batch = items[i : i + batch_size]
        batch_response = None
        last_error = None
        for model_name in candidate_models:
            try:
                batch_response = client.models.embed_content(
                    model=model_name,
                    contents=batch,
                    config=config
                )
                break
            except Exception as e:
                last_error = e
                print(f"[WARN] Embedding model {model_name} failed ({e}). Retrying with next candidate...")
                continue

        if batch_response is None:
            raise RuntimeError(f"All Gemini embedding models failed. Last error: {last_error}")

        for emb in batch_response.embeddings:
            embeddings.append(emb.values)

    return embeddings


def get_chroma_path() -> str:
    """
    Returns the persistent storage path for ChromaDB.
    Respects CHROMA_PERSIST_DIR for persistent volumes or defaults to project root chroma_db.
    """
    default_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "chroma_db"
    )
    return os.getenv("CHROMA_PERSIST_DIR", default_dir)


def get_collection_name(video_id: str) -> str:
    """
    Returns safe collection name format compliant with ChromaDB rules (starts with letter, no hyphens).
    """
    return f"vid_{video_id}".replace("-", "_")


def _chromadb_text_to_vector(document: str, video_id: str) -> dict:
    print(f"Storing embeddings for Video ID: {video_id} (Full transcript length: {len(document)} chars)")

    client = chromadb.PersistentClient(path=get_chroma_path())
    
    # Safe collection name format compliant with ChromaDB rules
    collection_name = get_collection_name(video_id)

    # Clear stale collection on re-ingestion
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=collection_name)

    try:
        text_split = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = text_split.split_text(document)

        print(f"Generated {len(chunks)} chunks for video_id: {video_id}")

        # Generate embeddings with explicit RETRIEVAL_DOCUMENT task type
        try:
            embeddings = get_gemini_embedding(chunks, task_type="RETRIEVAL_DOCUMENT")
        except TypeError:
            embeddings = get_gemini_embedding(chunks)

        ids = [f"{video_id}_chunk{i}" for i in range(len(chunks))]
        metadata = [{"video_id": video_id, "chunk_number": i} for i in range(len(chunks))]

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata
        )

        return {
            "message": f"[SUCCESS] {len(chunks)} chunks stored successfully using Gemini Embeddings!",
            "video_id": video_id,
            "total_chunks": len(chunks)
        }
    except Exception as e:
        print(f"[ERROR] Ingestion failed for video_id {video_id}: {e}")
        raise RuntimeError(f"ChromaDB ingestion failed: {e}") from e
