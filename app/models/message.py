from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID
from typing import List, Optional


class NewMessageModel(BaseModel):
    chat_id: UUID
    sender_id: UUID
    content: str

    class Config:
        from_attributes = True


class MessageModel(BaseModel):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str,  # Преобразуем UUID в строку
        }


# Модель для получения истории сообщений
class MessageHistoryModel(BaseModel):
    chat_id: UUID
    messages: List[MessageModel]  # Список сообщений в чате

    class Config:
        from_attributes = True
