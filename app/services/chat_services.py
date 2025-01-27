from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.chat_repository import get_chat_by_chat_id
from app.models.chat import ChatModel


async def get_chat(
    chat_id: UUID,
    db_session: AsyncSession,
    user_id: UUID,
    check_permission: bool = True,
) -> ChatModel:
    chat = await get_chat_by_chat_id(chat_id=chat_id, db_session=db_session)
    if not chat:
        raise HTTPException(status_code=400, detail="Chat not found")
    if check_permission and user_id not in chat.user_ids:
        raise HTTPException(status_code=403, detail="Permission denied")

    return chat
