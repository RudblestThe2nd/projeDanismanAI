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


