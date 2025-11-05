import os
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

INDEX_PATH = "faiss_index"

st.set_page_config(page_title="RAG Teaching Assistant", layout="wide")
st.title("RAG-based AI Teaching Assistant (Demo)")

# Sidebar
st.sidebar.header("Setup")
openai_key = st.sidebar.text_input("OpenAI API Key (sk-...)", type="password")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key

if st.sidebar.button("Ingest sample documents (build FAISS index)"):
    st.info("Run ingest.py locally or use Python execution environment to build the FAISS index.")
    st.write("Example: python ingest.py --input_dir sample_data --index_path faiss_index")

# Main
if not os.path.exists(INDEX_PATH):
    st.warning("FAISS index not found. Please run ingest.py to create the index using your OpenAI key.")
    st.info("Sample data is provided in /sample_data. After running ingest you can ask questions below.")
else:
    q = st.text_input("Ask a question about the course material:")
    if st.button("Get Answer"):
        if not q:
            st.warning("Enter a question.")
        else:
            embeddings = OpenAIEmbeddings()
            store = FAISS.load_local(INDEX_PATH, embeddings)
            retriever = store.as_retriever(search_kwargs={"k": 4})
            llm = OpenAI(temperature=0)
            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
            with st.spinner("Generating answer..."):
                resp = qa.run(q)
            st.subheader("Answer")
            st.write(resp)
            st.subheader("Retrieved Sources")
            docs = retriever.get_relevant_documents(q)
            for d in docs:
                st.write(d.metadata)
                st.write(d.page_content[:500] + ("..." if len(d.page_content)>500 else ""))