# app.py

import os
import streamlit as st

from ingestor import ingest
from chain import ask
from config import UPLOAD_DIR


def save_uploaded_file(uploaded_file) -> str:
    """Save the uploaded file to disk and return its path."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def main():
    st.set_page_config(
        page_title="Chat with your Documents",
        page_icon="📄",
        layout="centered"
    )

    st.title("📄 Chat with your Documents")
    st.markdown("Upload a PDF or text file and ask questions about it.")

    # --- Sidebar: file upload and ingestion ---
    with st.sidebar:
        st.header("Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt"]
        )

        if uploaded_file is not None:
            if st.button("Process Document"):
                with st.spinner("Processing document..."):
                    file_path = save_uploaded_file(uploaded_file)
                    ingest(file_path)
                    st.session_state["document_ready"] = True
                    st.success("Document processed! You can now ask questions.")

    # --- Main area: chat interface ---
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if st.session_state.get("document_ready"):

        # Display chat history
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        user_question = st.chat_input("Ask a question about your document...")

        if user_question:
            # Show user message
            st.session_state["chat_history"].append({
                "role": "user",
                "content": user_question
            })
            with st.chat_message("user"):
                st.markdown(user_question)

            # Get answer
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer, sources = ask(user_question)
                    st.markdown(answer)

                    # Show source chunks
                    with st.expander("Sources"):
                        for i, doc in enumerate(sources):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.markdown(doc.page_content)
                            st.divider()

            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": answer
            })

    else:
        st.info("Please upload and process a document from the sidebar to get started.")


if __name__ == "__main__":
    main()