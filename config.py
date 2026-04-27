# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# LLM settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Chunking settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retriever settings
TOP_K_RESULTS = 4

# Vector store settings
CHROMA_DB_DIR = "./chroma_db"

# Temporary upload folder
UPLOAD_DIR = "./data"