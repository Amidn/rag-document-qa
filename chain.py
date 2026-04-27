# chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma

from config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    EMBEDDING_MODEL,
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


def build_prompt():
    """Build the prompt template for the LLM."""
    return PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )


def build_llm():
    """Initialize the OpenAI LLM."""
    return ChatOpenAI(
        model=LLM_MODEL,
        openai_api_key=OPENAI_API_KEY,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )


def build_retriever():
    """Load the vector store and return a retriever object."""
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )

    return vector_store.as_retriever(
        search_kwargs={"k": TOP_K_RESULTS}
    )


def build_chain():
    """Assemble the full RAG chain."""
    llm = build_llm()
    prompt = build_prompt()
    retriever = build_retriever()

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return chain


def ask(question: str):
    """Ask a question and return the answer and source documents."""
    chain = build_chain()

    result = chain.invoke({"query": question})

    answer = result["result"]
    sources = result["source_documents"]

    return answer, sources