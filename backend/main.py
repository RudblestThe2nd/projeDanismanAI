import json
import re
import json as _json
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import io

from database import get_db, User, Conversation, Message, create_tables
from auth import hash_password, verify_password, create_access_token, get_current_user
from skill_router import detect_skill
from hf_client import call_hf_endpoint, build_prompt
from document_builder import metin_to_docx, json_to_docx
from file_processor import (
    extract_text, chunk_text, build_chunk_prompt,
    extract_sections_from_docx, extract_sections_from_pdf,
    keyword_match_sections,
)

app = FastAPI(title="ProjeDanışmanAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    create_tables()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    skill: Optional[str] = "otomatik"

class ConversationCreate(BaseModel):
    title: Optional[str] = "Yeni Sohbet"


@app.post("/auth/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı")
    user = User(email=req.email, hashed_password=hash_password(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Kayıt başarılı", "email": user.email}


@app.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}


@app.post("/conversations")
def create_conversation(req: ConversationCreate, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    conv = Conversation(user_id=current_user.id, title=req.title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"id": conv.id, "title": conv.title, "created_at": conv.created_at}


@app.get("/conversations")
def list_conversations(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    convs = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.desc()).all()
    return [{"id": c.id, "title": c.title, "created_at": c.created_at} for c in convs]


@app.get("/conversations/{conv_id}/messages")
def get_messages(conv_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    conv = db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")
    msgs = db.query(Message).filter(
        Message.conversation_id == conv_id
    ).order_by(Message.created_at).all()
    return [{"role": m.role, "content": m.content, "skill_used": m.skill_used,
             "created_at": m.created_at} for m in msgs]


@app.delete("/conversations/{conv_id}")
def delete_conversation(conv_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    conv = db.query(Conversation).filter(
        Conversation.id == conv_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")
    db.query(Message).filter(Message.conversation_id == conv_id).delete()
    db.delete(conv)
    db.commit()
    return {"message": "Sohbet silindi"}


@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db),
         current_user: User = Depends(get_current_user)):
    conv = db.query(Conversation).filter(
        Conversation.id == req.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")

    skill_name = req.skill if req.skill != "otomatik" else detect_skill(req.message)

    recent = db.query(Message).filter(
        Message.conversation_id == req.conversation_id
    ).order_by(Message.created_at.desc()).limit(4).all()
    history = [{"role": m.role, "content": m.content} for m in reversed(recent)]

    # Conversation'a bağlı belge varsa ilgili bölümleri mesaja ekle
    user_message = req.message
    if conv.document_sections:
        try:
            sections = json.loads(conv.document_sections)
            matched = keyword_match_sections(sections, req.message)
            if matched:
                user_message = (
                    f"{req.message}\n\n"
                    f"---\n"
                    f"BELGE METNİ ({conv.document_filename}):\n{matched}\n\n"
                    f"---\n"
                    f"Yanıt formatı:\n"
                    f"1. **Belgede ne yazıyor:** Metinden doğrudan alıntı yap.\n"
                    f"2. **Değerlendirme:** Alıntıya dayanarak Türkçe yaz.\n"
                    f"KURAL: Belgede olmayan bilgi ekleme. İngilizce kullanma."
                )
            elif sections:
                toc = "\n".join(f"- {h}" for h in sections if h != "__giris__")
                user_message = (
                    f"{req.message}\n\n"
                    f"---\n"
                    f"Not: '{conv.document_filename}' belgesi bu sohbete yüklendi ancak "
                    f"sorulan konu belgede ayrı başlık olarak bulunmuyor.\n"
                    f"Belgede yer alan bölümler:\n{toc}"
                )
        except Exception:
            pass

    messages = build_prompt(skill_name, history, user_message)
    response_text = call_hf_endpoint(messages)

    db.add(Message(conversation_id=req.conversation_id, role="user",
                   content=req.message, skill_used=skill_name))
    db.add(Message(conversation_id=req.conversation_id, role="assistant",
                   content=response_text, skill_used=skill_name))

    if conv.title == "Yeni Sohbet":
        conv.title = req.message[:40] + ("..." if len(req.message) > 40 else "")

    db.commit()
    return {"response": response_text, "skill_used": skill_name}


@app.post("/chat/upload")
async def chat_upload(
    file: UploadFile = File(...),
    conversation_id: int = Form(...),
    instruction: str = Form("Bu belgeyi analiz et ve TEKNOFEST/TÜBİTAK açısından değerlendir."),
    skill: str = Form("otomatik"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Dosya çok büyük. Maksimum 10MB.")

    try:
        text = extract_text(file_bytes, file.filename)
    except (ValueError, ImportError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text.strip():
        raise HTTPException(status_code=400, detail="Dosyadan metin çıkarılamadı.")

    skill_name = skill if skill != "otomatik" else detect_skill(instruction)

    user_msg_content = f"📎 **{file.filename}** yüklendi\n\n{instruction}"
    db.add(Message(conversation_id=conversation_id, role="user",
                   content=user_msg_content, skill_used=skill_name))
    if conv.title == "Yeni Sohbet":
        conv.title = f"📎 {file.filename[:35]}"

    # Bölüm bazlı akıllı arama: önce ilgili bölümleri bul, tek seferde analiz et
    matched_content = ""
    sections = {}
    fname_lower = file.filename.lower()
    try:
        if fname_lower.endswith(".docx"):
            sections = extract_sections_from_docx(file_bytes)
            matched_content = keyword_match_sections(sections, instruction)
        elif fname_lower.endswith(".pdf"):
            sections = extract_sections_from_pdf(file_bytes)
            matched_content = keyword_match_sections(sections, instruction)
    except Exception:
        matched_content = ""

    # Belge bölümlerini conversation'a kaydet (sonraki mesajlarda tekrar erişim için)
    if sections:
        conv.document_sections = json.dumps(sections, ensure_ascii=False)
        conv.document_filename = file.filename
    db.commit()

    if matched_content:
        # İlgili bölümler bulundu — tek API çağrısı, loop yok
        prompt = (
            f"Görev: {instruction}\n\n"
            f"---\n"
            f"BELGE METNİ:\n{matched_content}\n\n"
            f"---\n"
            f"Yanıt formatı (bu formatı kesinlikle uygula):\n"
            f"1. **Belgede ne yazıyor:** Yukarıdaki metinden doğrudan alıntı yap (değiştirme).\n"
            f"2. **Değerlendirme:** Alıntıya dayanarak Türkçe olarak eksik, güçlü ve zayıf yönleri yaz.\n\n"
            f"KURAL: Belgede YER ALMAYAN bilgi, bölüm veya sayı ekleme. "
            f"Sadece yukarıdaki metni kaynak al. İngilizce kullanma."
        )
        messages = build_prompt(skill_name, [], prompt)
        response = call_hf_endpoint(messages)
        db.add(Message(conversation_id=conversation_id, role="assistant",
                       content=response, skill_used=skill_name))
        db.commit()
        return {
            "response": response,
            "skill_used": skill_name,
            "chunk_index": 0,
            "total_chunks": 1,
            "filename": file.filename,
            "instruction": instruction,
            "remaining_chunks": [],
            "has_more": False,
        }

    if sections:
        # Bölümler çıkarıldı ama eşleşme yok — ilgili bölüm belgede yok
        toc = "\n".join(f"- {h}" for h in sections if h != "__giris__")
        response = (
            f"Bu belgede aradığınız bölüm ayrı bir başlık olarak **bulunmuyor**.\n\n"
            f"Belgede yer alan bölümler:\n{toc}\n\n"
            f"Belirtilen bölümlerden birini analiz etmemi ister misiniz?"
        )
        db.add(Message(conversation_id=conversation_id, role="assistant",
                       content=response, skill_used=skill_name))
        db.commit()
        return {
            "response": response,
            "skill_used": skill_name,
            "chunk_index": 0,
            "total_chunks": 1,
            "filename": file.filename,
            "instruction": instruction,
            "remaining_chunks": [],
            "has_more": False,
        }

    # Fallback: başlık yapısı çıkarılamadıysa chunk akışı
    chunks = chunk_text(text, chunk_size=2000, overlap=150)
    chunk_prompt = build_chunk_prompt(instruction, chunks[0], 0, len(chunks))
    messages = build_prompt(skill_name, [], chunk_prompt)
    response = call_hf_endpoint(messages)

    if len(chunks) > 1:
        response += f"\n\n---\n📄 **Bölüm 1/{len(chunks)} tamamlandı.** Devam edeyim mi?"

    db.add(Message(conversation_id=conversation_id, role="assistant",
                   content=response, skill_used=skill_name))
    db.commit()

    return {
        "response": response,
        "skill_used": skill_name,
        "chunk_index": 0,
        "total_chunks": len(chunks),
        "filename": file.filename,
        "instruction": instruction,
        "remaining_chunks": chunks[1:],
        "has_more": len(chunks) > 1,
    }


@app.post("/chat/upload/continue")
async def chat_upload_continue(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    body = await request.json()
    conversation_id = body.get("conversation_id")
    chunk           = body.get("chunk", "")
    chunk_index     = body.get("chunk_index", 1)
    total_chunks    = body.get("total_chunks", 1)
    filename        = body.get("filename", "")
    instruction     = body.get("instruction", "")
    skill           = body.get("skill", "otomatik")

    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")

    skill_name   = skill if skill != "otomatik" else detect_skill(instruction)
    chunk_prompt = build_chunk_prompt(instruction, chunk, chunk_index, total_chunks)
    messages     = build_prompt(skill_name, [], chunk_prompt)
    response     = call_hf_endpoint(messages)

    is_last = chunk_index == total_chunks - 1

    if not is_last:
        response += f"\n\n---\n📄 **Bölüm {chunk_index + 1}/{total_chunks} tamamlandı.** Devam edeyim mi?"
    else:
        response += f"\n\n---\n✅ **Tüm belge analizi tamamlandı ({total_chunks} bölüm).**"

    db.add(Message(conversation_id=conversation_id, role="assistant",
                   content=response, skill_used=skill_name))
    db.commit()

    return {
        "response": response,
        "skill_used": skill_name,
        "chunk_index": chunk_index,
        "total_chunks": total_chunks,
        "has_more": not is_last,
    }


@app.post("/chat/word")
def chat_word(req: ChatRequest, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    conv = db.query(Conversation).filter(
        Conversation.id == req.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")

    last_msg = db.query(Message).filter(
        Message.conversation_id == req.conversation_id,
        Message.role == "assistant"
    ).order_by(Message.created_at.desc()).first()

    if not last_msg:
        raise HTTPException(status_code=404, detail="İndirilecek mesaj bulunamadı")

    response_text = last_msg.content

    try:
        temiz = re.sub(r"```json|```", "", response_text).strip()
        veri  = json.loads(temiz)
        if "proje_adi" in veri and "bolumler" in veri:
            docx_bytes = json_to_docx(veri)
        else:
            raise ValueError("JSON var ama beklenen format değil")
    except Exception:
        docx_bytes = metin_to_docx(
            response_text,
            proje_adi=conv.title or "ProjeDanışmanAI Raporu",
            takim_adi=current_user.email.split("@")[0],
        )

    return StreamingResponse(
        io.BytesIO(docx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=projedanismanai_rapor.docx"}
    )


@app.post("/chat/pdf")
def chat_pdf(req: ChatRequest, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    conv = db.query(Conversation).filter(
        Conversation.id == req.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı")

    last_msg = db.query(Message).filter(
        Message.conversation_id == req.conversation_id,
        Message.role == "assistant"
    ).order_by(Message.created_at.desc()).first()

    if not last_msg:
        raise HTTPException(status_code=404, detail="İndirilecek mesaj bulunamadı")

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import os

        font_dir = "/usr/share/fonts/truetype/dejavu/"
        if not os.path.exists(font_dir + "DejaVuSans.ttf"):
            raise ImportError("DejaVu font bulunamadı")

        pdfmetrics.registerFont(TTFont("DejaVu",      font_dir + "DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", font_dir + "DejaVuSans-Bold.ttf"))

        buf = io.BytesIO()
        doc_pdf = SimpleDocTemplate(buf, pagesize=A4,
                                    leftMargin=3*cm, rightMargin=2.5*cm,
                                    topMargin=2.5*cm, bottomMargin=2.5*cm)

        stil_govde  = ParagraphStyle("govde",  fontName="DejaVu", fontSize=11, leading=17, spaceAfter=8)
        stil_baslik = ParagraphStyle("baslik", fontName="DejaVu-Bold", fontSize=14,
                                     textColor=colors.HexColor("#1F3864"), spaceAfter=6, spaceBefore=14)

        icerik = []
        for satir in last_msg.content.split("\n"):
            satir = satir.strip()
            if not satir:
                icerik.append(Spacer(1, 0.3*cm))
            elif satir.startswith("# ") or satir.startswith("## ") or satir.startswith("### "):
                icerik.append(Paragraph(satir.lstrip("# "), stil_baslik))
            else:
                satir = satir.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                icerik.append(Paragraph(satir, stil_govde))

        doc_pdf.build(icerik)
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=projedanismanai_rapor.pdf"}
        )

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"PDF üretimi başarısız: {str(e)}. /chat/word kullanın.")


@app.get("/skills")
def list_skills():
    return [
        {"value": "otomatik",                          "label": "Otomatik Tespit"},
        {"value": "project_idea_refinement",           "label": "Proje Fikri Netleştirme"},
        {"value": "report_section_writer",             "label": "Rapor Bölümü Yazma"},
        {"value": "tubitak_application_guidance",      "label": "TÜBİTAK Başvuru Rehberliği"},
        {"value": "teknofest_ktr_ptr_guidance",        "label": "TEKNOFEST KTR/PTR"},
        {"value": "feasibility_and_risk_check",        "label": "Uygulanabilirlik ve Risk"},
        {"value": "title_abstract_generator",          "label": "Başlık ve Özet"},
        {"value": "presentation_and_jury_preparation", "label": "Sunum ve Jüri Hazırlığı"},
    ]


@app.get("/health")
def health():
    return {"status": "ok"}
