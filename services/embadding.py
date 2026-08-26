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

