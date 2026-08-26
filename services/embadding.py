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

