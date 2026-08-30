from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, event
from sqlalchemy import text as sa_text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./projeDanismanAI.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    conversations = relationship("Conversation", back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, default="Yeni Sohbet")
    created_at = Column(DateTime, default=datetime.utcnow)
    document_sections = Column(Text, nullable=True)   # JSON: {başlık: içerik}
    document_filename = Column(String, nullable=True)
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String, nullable=False)  # 'user' veya 'assistant'
    content = Column(Text, nullable=False)
    skill_used = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
    # Mevcut DB'ye yeni kolonları ekle (SQLite ALTER TABLE)
    with engine.connect() as conn:
        existing = [row[1] for row in conn.execute(sa_text("PRAGMA table_info(conversations)")).fetchall()]
        if "document_sections" not in existing:
            conn.execute(sa_text("ALTER TABLE conversations ADD COLUMN document_sections TEXT"))
        if "document_filename" not in existing:
            conn.execute(sa_text("ALTER TABLE conversations ADD COLUMN document_filename VARCHAR"))
        conn.commit()