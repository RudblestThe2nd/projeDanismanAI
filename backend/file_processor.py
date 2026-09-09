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


_NUMBERED_HEADING = re.compile(r"^\d+(\.\d+)*[\.\s]")


def _is_heading_para(para) -> bool:
    """Paragrafın başlık olup olmadığını belirler (stil, bold, numaralı)."""
    style_lower = para.style.name.lower()
    heading_styles = {"heading", "başlık", "title", "subtitle"}
    if any(h in style_lower for h in heading_styles):
        return True
    text = para.text.strip()
    if not text or len(text) > 120:
        return False
    # Tüm runs bold ise ve kısa ise başlık say
    runs = [r for r in para.runs if r.text.strip()]
    if runs and all(r.bold for r in runs):
        return True
    # "1." / "1.1." / "7.3." gibi numaralı kısa satırlar
    if _NUMBERED_HEADING.match(text) and len(text) < 100:
        return True
    return False


def extract_sections_from_docx(file_bytes: bytes) -> Dict[str, str]:
    """DOCX'ten {başlık: içerik} dict'i döner. Heading stili, bold ve numaralı başlıkları yakalar."""
    from docx import Document
    doc = Document(io.BytesIO(file_bytes))

    sections: Dict[str, str] = {}
    current_heading = "__giris__"
    current_lines: List[str] = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if _is_heading_para(para):
            if current_lines:
                sections[current_heading] = "\n".join(current_lines)
            current_heading = text
            current_lines = []
        else:
            current_lines.append(text)

    if current_lines:
        sections[current_heading] = "\n".join(current_lines)

    return sections


def extract_sections_from_pdf(file_bytes: bytes) -> Dict[str, str]:
    """PDF'ten sayfa bazlı bölümler çıkarır."""
    import pypdf
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    sections: Dict[str, str] = {}
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            sections[f"Sayfa {i + 1}"] = text.strip()
    return sections


_TR_STOPWORDS = {
    "mi", "mı", "mu", "mü", "bir", "bu", "şu", "ve", "ile", "de", "da",
    "ki", "ya", "için", "ama", "fakat", "ancak", "var", "yok", "ne",
    "nasıl", "hangi", "neden", "sen", "ben", "biz", "siz", "değil",
    "gibi", "kadar", "daha", "en", "çok", "az", "sence", "bana", "bence",
    "acaba", "olan", "ile", "veya", "ya", "da", "bile", "misin", "musun",
    "mısın", "misiniz", "kısmını", "kısmı", "bölümünü", "bölümü",
    "değerlendirir", "değerlendirmisin", "değerlendirme", "incelemisin",
    "bakabilir", "bakarmısın", "söyler", "anlatır", "hakkında", "konusunda",
    "ilgili", "olan", "olarak", "olan", "göre", "kadar", "sonra", "önce",
}

_TR_SUFFIXES = (
    "ları", "leri", "ını", "ini", "unu", "ünü", "nın", "nin", "nun", "nün",
    "ında", "inde", "unda", "ünde", "dan", "den", "tan", "ten", "nda", "nde",
    "la", "le", "ya", "ye", "a", "e", "ı", "i", "u", "ü",
)


def _stem_tr(word: str) -> str:
    """Yaygın Türkçe ekleri kaldırır (basit yaklaşım)."""
    for suffix in _TR_SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def _normalize_typos(word: str) -> str:
    """Ardışık tekrar eden harfleri tek harfe indirir (alggoritma → algoritma)."""
    return re.sub(r'(.)\1+', r'\1', word)


def extract_query_keywords(query: str) -> List[str]:
    """Sorgudan anlamlı Türkçe kelimeleri çıkarır, kök formuna indirir."""
    words = re.findall(r'\b\w+\b', query.lower())
    stems = set()
    for w in words:
        w = _normalize_typos(w)
        if len(w) > 2 and w not in _TR_STOPWORDS:
            stems.add(_stem_tr(w))
    return list(stems)


def keyword_match_sections(
    sections: Dict[str, str],
    query: str,
    max_sections: int = 3,
    max_chars: int = 5000,
) -> str:
    """
    Sorguyla eşleşen bölümleri bulur ve birleşik metin olarak döner.
    Önce başlıkta keyword ara (birincil). Bulamazsa içeriğe bak (ikincil).
    Boş string dönerse fallback chunk yaklaşımı kullanılmalı.
    """
    keywords = extract_query_keywords(query)
    if not keywords:
        return ""

    primary: List[tuple] = []   # başlıkta eşleşme var
    secondary: List[tuple] = [] # sadece içerikte eşleşme var

    for heading, content in sections.items():
        if heading == "__giris__":
            continue
        h_lower = heading.lower()
        c_lower = content.lower()
        h_score = sum(1 for kw in keywords if kw in h_lower)
        c_score = sum(1 for kw in keywords if kw in c_lower)

        if h_score > 0:
            primary.append((h_score * 3 + c_score, heading, content))
        elif c_score >= 2:
            secondary.append((c_score, heading, content))

    primary.sort(key=lambda x: x[0], reverse=True)
    secondary.sort(key=lambda x: x[0], reverse=True)

    # Başlık eşleşmesi varsa onu kullan, yoksa içerik eşleşmesine düş
    candidates = primary if primary else secondary
    if not candidates:
        return ""

    parts = []
    total_chars = 0
    for _, heading, content in candidates[:max_sections]:
        block = f"## {heading}\n{content}"
        if total_chars + len(block) > max_chars:
            block = block[: max_chars - total_chars]
        parts.append(block)
        total_chars += len(block)
        if total_chars >= max_chars:
            break

    return "\n\n".join(parts)


def chunk_text(text: str, chunk_size: int = 3000, overlap: int = 200) -> List[str]:
    """
    Metni chunk_size karakterlik parçalara böler.
    overlap: ardışık chunk'lar arasında tekrar eden karakter sayısı (bağlam sürekliliği).
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size

        # Kelime ortasında kesmemek için en yakın boşluğa git
        if end < len(text):
            last_space = text.rfind(" ", start, end)
            if last_space > start:
                end = last_space

        chunks.append(text[start:end].strip())
        start = end - overlap  # overlap kadar geri dön

    return [c for c in chunks if c.strip()]


def build_chunk_prompt(
    user_instruction: str,
    chunk: str,
    chunk_index: int,
    total_chunks: int,
) -> str:
    """Her chunk için modele gönderilecek prompt'u oluşturur."""
    if total_chunks == 1:
        return f"{user_instruction}\n\n---\nBELGE İÇERİĞİ:\n{chunk}"

    if chunk_index == total_chunks - 1:
        suffix = "Bu son bölüm. Tüm bölümlerdeki bulgularını özetle ve kullanıcının sorusuna net bir sonuç ver."
    else:
        suffix = "Sadece bu bölümde kullanıcının sorusuyla ilgili bilgileri kısaca çıkar. Tekrar etme, yorum katma."

    return (
        f"Kullanıcının sorusu: {user_instruction}\n\n"
        f"---\n"
        f"BELGE BÖLÜMÜ {chunk_index + 1}/{total_chunks}:\n"
        f"{chunk}\n\n"
        f"---\n{suffix}"
    )
