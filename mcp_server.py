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

