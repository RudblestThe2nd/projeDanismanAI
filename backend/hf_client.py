import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_ENDPOINT = os.getenv("HF_ENDPOINT", "")
HF_TOKEN    = os.getenv("HF_TOKEN", "")

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PROMPT_DIR = os.path.join(BASE_DIR, "prompt_system")

SYSTEM_PROMPT = """Sen ProjeDanışmanAI'sın. TEKNOFEST ve TÜBİTAK yarışmacılarına Türkçe olarak \
rehberlik eden bir yapay zeka danışmanısın.
Görevin: proje fikri geliştirme, teknik rapor (KTR/PTR) yazımı, strateji \
belirleme, hata düzeltme ve başvuru süreçleri konularında net, uygulanabilir \
ve detaylı yanıtlar vermek.
Yalnızca TEKNOFEST, TÜBİTAK ve bağlantılı mühendislik/bilim proje konularında \
yardım et. Alan dışı sorularda kibarca reddet.
ÖNEMLI: Her zaman Türkçe yanıt ver. İngilizce kullanma."""

BAD_RESPONSE_PATTERNS = [
    "Model hatası",
    "Bağlantı",
    "Zaman aşımı",
    "Merhaba! Bu platformda",
    "Bu platformda TÜBİTAK",
    "[DEMO MODU]",
]

def _is_bad_assistant_response(content: str) -> bool:
    return any(content.strip().startswith(p) for p in BAD_RESPONSE_PATTERNS)


def read_file(path: str) -> str:
    full_path = os.path.join(PROMPT_DIR, path)
    if os.path.exists(full_path):
        with open(full_path, encoding="utf-8") as f:
            return f.read()
    return ""


def _clean_response(text: str) -> str:
    # Remove complete <think>...</think> blocks
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    # Remove unclosed <think> block (model cut off mid-think)
    text = re.sub(r"<think>.*", "", text, flags=re.DOTALL)
    return text.strip()


