import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb
from sentence_transformers import SentenceTransformer

from config import GOOGLE_API_KEY
from config import HF_TOKEN

# Lazy loading model singleton
_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = SentenceTransformer("all-MiniLM-L6-v2")
    return _model_instance

def _gemini_text_to_vector(document: str):
    """ this function user for conver long text into small chunks and srote them to a vector database"""
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    try:
        embaddings = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        chunks = text_splitter.split_text(document)
        for chunk in chunks:
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=chunk
            )
            embaddings.append(response.embeddings[0].values)
    except Exception as e:
        print(f"Error:{e}")
        embaddings = []

    return embaddings

def _chromadb_text_to_vector(document: str, video_id: str):
    print(f"Storing embeddings for Video ID: {video_id} (Full transcript length: {len(document)} chars)")

    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if re-ingesting to clear stale tiny chunks
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

        # generate embedding lazily
        model = get_model()
        embadding = model.encode(chunks).tolist()

        # generate ids
        ids = [f"{video_id}_chunk{i}" for i in range(len(chunks))]

        # metadata
        metadata = [{
            "video_id": video_id,
            "chunk_number": i
        } for i in range(len(chunks))]

        # store data in chromaDB
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embadding,
            metadatas=metadata
        )

        return {
            "message": f"[SUCCESS] {len(chunks)} chunks stored successfully across complete video transcript!",
            "video_id": video_id,
            "total_chunks": len(chunks)
        }
    except Exception as e:
        raise Exception(f"error: {e}")
