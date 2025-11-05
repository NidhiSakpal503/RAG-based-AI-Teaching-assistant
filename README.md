# RAG-based AI Teaching Assistant (Demo)

## Overview
A simple Retrieval-Augmented Generation (RAG) teaching assistant prototype using:
- Python + LangChain
- OpenAI API (for LLM)
- FAISS (local vector store) for retrieval
- Streamlit for the web UI

Features:
- Upload course documents (PDF / TXT)
- Ingest and create embeddings (local FAISS)
- Ask contextual questions with retrieved passages
- Lightweight demo intended for portfolio / academic use

## Files
- `app.py` - Streamlit web app (UI + QA loop)
- `ingest.py` - Document ingestion & FAISS index building
- `utils.py` - helper functions for text extraction and chunking
- `requirements.txt` - Python dependencies
- `sample_data/sample_course.txt` - example course material
- `README.md` - this file

## Quick start (local)
1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key in the environment:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Notes
- This project uses local FAISS for vector storage (no managed vector DB required).
- Replace or extend `sample_data/` with your own PDFs/TXT files before ingestion.
- For production use, consider a managed vector DB (Pinecone, Weaviate) and secure secret handling.