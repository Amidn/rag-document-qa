# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# LLM settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"
MAX_TOKENS = 1000
TEMPERATURE = 0.0

# Embedding settings
EMBEDDING_MODEL = "text-embedding-3-small"

# Document chunking settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retriever settings
TOP_K_RESULTS = 4

# Vector store settings
CHROMA_DB_DIR = "./chroma_db"

# Temporary upload folder
UPLOAD_DIR = "./data"