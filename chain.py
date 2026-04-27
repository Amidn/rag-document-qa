# chain.py

import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    CHROMA_DB_DIR,
    TOP_K_RESULTS
)

PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions based strictly on the provided context.
If the answer is not found in the context, say "I don't have enough information in the document to answer this question."
Do not make up answers.

Context:
{context}

Question:
{question}

Answer:
"""


def build_chain():
    """Assemble the full RAG chain using Groq and LCEL."""

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": TOP_K_RESULTS}
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def ask(question: str):
    """Ask a question and return the answer and source documents."""
    chain, retriever = build_chain()
    answer = chain.invoke(question)
    sources = retriever.invoke(question)
    return answer, sources