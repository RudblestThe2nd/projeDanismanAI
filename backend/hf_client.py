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


def call_hf_endpoint(messages: list) -> str:
    for msg in messages:
        if len(msg["content"]) > 6000:
            msg["content"] = msg["content"][:6000] + "\n...[metin kısaltıldı]"

    if not HF_ENDPOINT or "buraya" in HF_ENDPOINT:
        return (
            "**[DEMO MODU]** Model henüz bağlı değil.\n\n"
            f"Gönderilen mesaj sayısı: {len(messages)}"
        )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "model":            "Rudblest/projedanismanai-v2-qwen3-14b",
        "messages":         messages,
        "max_tokens":       600,
        "temperature":      0.3,
        "repetition_penalty": 1.2,
        "stream":           False,
    }

    try:
        r = requests.post(
            f"{HF_ENDPOINT}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=300,
        )

        print(f"HF status: {r.status_code}")
        print(f"HF response: {r.text[:300]}")

        if r.status_code == 200:
            content = r.json()["choices"][0]["message"]["content"]
            return _clean_response(content)

        return f"Model hatası: {r.status_code} — {r.text[:200]}"

    except requests.exceptions.Timeout:
        return "Zaman aşımı. Endpoint meşgul olabilir, tekrar dene."
    except requests.exceptions.ConnectionError:
        return "Bağlantı hatası. Endpoint URL'sini kontrol et."
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"


