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


