from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CreateChatModel(BaseModel):
    title: str = Field(max_length=50)
    slug: str = None

    @field_validator("slug", mode="before")
    def generate_slug(cls, v, values):
        # Проверяем, что slug не установлен, и генерируем его на основе title
        if v is None and "title" in values:
            return values["title"].replace(" ", "-").lower()
        return v


# Модель для чатов
class ChatModel(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    user_ids: list[UUID]  # Список участников чата

    class Config:
        from_attributes = True


class UsersInChatModel(BaseModel):
    chat_id: UUID
    is_add: bool
