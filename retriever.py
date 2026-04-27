# retriever.py

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DB_DIR,
    TOP_K_RESULTS
)


def load_vector_store():
    """Load the existing ChromaDB vector store from disk."""
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )

    return vector_store


def retrieve(query: str):
    """Search the vector store and return the most relevant chunks."""
    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        query=query,
        k=TOP_K_RESULTS
    )

    return results


def retrieve_with_scores(query: str):
    """Same as retrieve() but also returns similarity scores."""
    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        query=query,
        k=TOP_K_RESULTS
    )

    return results