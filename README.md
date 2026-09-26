# ProjeDanışmanAI

ProjeDanışmanAI, TEKNOFEST ve TÜBİTAK odaklı proje geliştirme süreçlerinde fikir netleştirme, teknik rapor yazımı, fizibilite/risk analizi, başvuru rehberliği ve jüri hazırlığı sunan yapay zekâ destekli bir danışmanlık uygulamasıdır.

## Teknoloji Yığını

- **Backend:** FastAPI, SQLAlchemy, JWT, Hugging Face Inference Endpoint
- **Frontend:** React, Vite, Axios, React Router, React Markdown
- **Doküman İşleme:** PDF, DOCX ve TXT metin çıkarımı ve parça bazlı analiz

## Yerel Kurulum

1. `backend/.env.example` dosyasını `backend/.env` olarak kopyalayın ve kendi değerlerinizi girin.
2. Backend bağımlılıklarını `pip install -r backend/requirements.txt` ile kurun.
3. Frontend bağımlılıklarını `cd frontend && npm install` ile kurun.
4. Backend ve frontend servislerini ayrı terminallerde başlatın.

> `.env`, yerel veritabanları ve kullanıcı verileri repository içinde tutulmaz.
