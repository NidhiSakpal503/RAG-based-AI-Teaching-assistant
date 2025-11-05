"""Ingest documents into a FAISS store using LangChain embeddings.

Usage:
    python ingest.py --input_dir sample_data --index_path faiss_index"
"""
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from utils import load_document, chunk_text

def ingest_directory(input_dir, index_path="faiss_index"):
    texts = []
    metadata = []
    for fname in os.listdir(input_dir):
        fpath = os.path.join(input_dir, fname)
        if not os.path.isfile(fpath): continue
        try:
            txt = load_document(fpath)
        except Exception as e:
            print("Skipping", fpath, ":", e)
            continue
        chunks = chunk_text(txt)
        for i, c in enumerate(chunks):
            texts.append(c)
            metadata.append({"source": fname, "chunk": i})
    embeddings = OpenAIEmbeddings()
    docs = [Document(page_content=t, metadata=m) for t,m in zip(texts, metadata)]
    store = FAISS.from_documents(docs, embeddings)
    store.save_local(index_path)
    print(f"Ingested {len(docs)} chunks to {index_path}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--input_dir", default="sample_data")
    p.add_argument("--index_path", default="faiss_index")
    args = p.parse_args()
    ingest_directory(args.input_dir, args.index_path)