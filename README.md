# 📄 RAG Document QA

A conversational question-answering app that lets you chat with your own documents using **Retrieval-Augmented Generation (RAG)** and **Large Language Models (LLMs)**.

Upload a PDF or text file, ask questions in natural language, and get accurate answers grounded strictly in your document — no hallucination.

---

## 🧠 How it works

1. **Ingest** — the document is loaded, split into chunks, and embedded into a local vector database (ChromaDB)
2. **Retrieve** — when you ask a question, the most relevant chunks are retrieved using semantic similarity search
3. **Generate** — the retrieved chunks are passed to an LLM (GPT-4o-mini) which generates a grounded answer

---

## 🛠️ Tech stack

| Component | Technology |
|---|---|
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector store | ChromaDB |
| RAG framework | LangChain |
| UI | Streamlit |
| Language | Python 3.11 |

---

## 📁 Project structure

rag-document-qa/
├── app.py           # Streamlit UI — main entry point
├── ingestor.py      # Document loading, chunking, and embedding
├── retriever.py     # Semantic search over the vector store
├── chain.py         # LLM chain — retrieval + answer generation
├── config.py        # Centralized settings
├── data/            # Temporary folder for uploaded documents
├── requirements.txt # Python dependencies
└── .env             # API keys (never pushed to GitHub)


---

## ⚙️ Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/rag-document-qa.git
cd rag-document-qa
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create your `.env` file**
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

**5. Run the app**
```bash
streamlit run app.py
```

---

## 💬 Usage

1. Open the app in your browser (Streamlit will open it automatically)
2. Upload a PDF or `.txt` file from the sidebar
3. Click **Process Document** and wait for it to finish
4. Start asking questions in the chat box

---

## 🔍 Features

- Supports PDF and plain text files
- Answers are grounded strictly in the uploaded document
- Shows source chunks used to generate each answer
- Clean chat interface with conversation history
- Modular codebase — easy to extend with new file types or LLMs

---

## 📌 Notes

- Your API key is never stored or pushed to GitHub
- The vector database is stored locally in `./chroma_db`
- To reset and upload a new document, delete the `./chroma_db` folder and restart the app