from typing import List, Dict, Any, Optional
import os
import uuid
from app.rag.chunking import chunk_text, chunk_by_paragraphs
from app.rag.embedding import embed_documents


async def ingest_text(
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    provider: str = None,
) -> List[Dict[str, Any]]:
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    documents = []
    
    for i, chunk in enumerate(chunks):
        doc = {
            "id": str(uuid.uuid4()),
            "content": chunk,
            "metadata": metadata or {},
            "chunk_index": i,
            "total_chunks": len(chunks),
        }
        documents.append(doc)
    
    if documents:
        documents = await embed_documents(documents, provider)
    
    return documents


async def ingest_file(
    file_path: str,
    metadata: Optional[Dict[str, Any]] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    provider: str = None,
) -> List[Dict[str, Any]]:
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt' or ext == '.md':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    return await ingest_text(text, metadata, chunk_size, chunk_overlap, provider)


def extract_text_from_pdf(file_path: str) -> str:
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except ImportError:
        raise ValueError("pdfplumber not installed. Run: pip install pdfplumber")


def extract_text_from_docx(file_path: str) -> str:
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except ImportError:
        raise ValueError("python-docx not installed. Run: pip install python-docx")