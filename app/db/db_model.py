import uuid

from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


class User(Base):
    """
    Модель пользователя
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    messages = relationship("Message", back_populates="sender")


class Chat(Base):
    """
    Модель чата
    """

    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(50))
    created_at = Column(TIMESTAMP, default=func.now())
    user_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    slug = Column(String, nullable=False)

    messages = relationship("Message", back_populates="chat")

    def get_messages(self):
        return self.messages


class Message(Base):
    """
    Модель сообщения
    """

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, default=func.now())

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")
