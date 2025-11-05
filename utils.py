import os
from PyPDF2 import PdfReader

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path):
    text = []
    reader = PdfReader(file_path)
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def load_document(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".txt", ".md"]:
        return read_txt(path)
    elif ext == ".pdf":
        return read_pdf(path)
    else:
        raise ValueError("Unsupported file type: " + ext)

def chunk_text(text, chunk_size=500, overlap=50):
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks