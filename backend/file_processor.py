"""
file_processor.py
PDF ve DOCX dosyalarından metin çıkarır, chunk'lara böler.
ProjeDanışmanAI v2
"""

import io
import re
from typing import List, Dict


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """PDF'ten düz metin çıkarır."""
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append(f"[Sayfa {i+1}]\n{text.strip()}")
        return "\n\n".join(pages)
    except ImportError:
        raise ImportError("pypdf kurulu değil. 'pip install pypdf' çalıştır.")
    except Exception as e:
        raise ValueError(f"PDF okuma hatası: {str(e)}")


def extract_text_from_docx(file_bytes: bytes) -> str:
    """DOCX'ten düz metin çıkarır."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text.strip())
        return "\n\n".join(paragraphs)
    except ImportError:
        raise ImportError("python-docx kurulu değil. 'pip install python-docx' çalıştır.")
    except Exception as e:
        raise ValueError(f"DOCX okuma hatası: {str(e)}")


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Dosya türüne göre metin çıkarır."""
    fname = filename.lower()
    if fname.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif fname.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif fname.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Desteklenmeyen dosya türü: {filename}. PDF, DOCX veya TXT yükle.")


