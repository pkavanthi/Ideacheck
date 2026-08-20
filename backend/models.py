from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.database import Base


class ContentType(str, enum.Enum):
    """Content type enumeration"""
    LECTURE = "lecture"
    ASSIGNMENT = "assignment"
    READING = "reading"
    EXAM = "exam"
    OTHER = "other"


class LanguageCode(str, enum.Enum):
    """Supported language codes"""
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    ZH = "zh"
    JA = "ja"
    KO = "ko"
    AR = "ar"
    HI = "hi"
    PT = "pt"


class Content(Base):
    """Educational content model"""
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    content_type = Column(Enum(ContentType), nullable=False)
    original_language = Column(Enum(LanguageCode), nullable=False)
    original_text = Column(Text, nullable=False)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    translations = relationship("Translation", back_populates="content", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', type={self.content_type})>"


class Translation(Base):
    """Translation model for educational content"""
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, index=True)
    target_language = Column(Enum(LanguageCode), nullable=False, index=True)
    translated_text = Column(Text, nullable=False)
    translated_title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    content = relationship("Content", back_populates="translations")

    def __repr__(self):
        return f"<Translation(id={self.id}, content_id={self.content_id}, language={self.target_language})>"
