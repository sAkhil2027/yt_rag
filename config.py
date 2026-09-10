import os
from dotenv import load_dotenv

load_dotenv()

# Prevent ChromaDB telemetry network delays on startup
os.environ.setdefault("ANONYMOUS_TELEMETRY", "False")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")
