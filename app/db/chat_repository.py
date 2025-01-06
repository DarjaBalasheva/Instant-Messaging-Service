from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_model import Chat
from app.models.chat import CreateChatModel
from sqlalchemy.dialects.postgresql import UUID


async def get_all_chats_by_user_id(db_session: AsyncSession,
                                   user_id: UUID) -> Sequence[Chat]:

    stmt = select(Chat).where(Chat.user_ids.any(user_id))
    result = await db_session.execute(stmt)
    chats = result.scalars().all()
    return chats


async def get_chat_by_chat_id(chat_id: UUID,
                              db_session: AsyncSession) -> Chat:

    stmt = select(Chat).where(Chat.id == chat_id)
    result = await db_session.execute(stmt)
    chat = result.scalars().first()
    return chat


def create_new_chat(chat: CreateChatModel,
                    db_session: AsyncSession,
                    user_ids: list[UUID]):

    chat = Chat(**chat.dict(), user_ids=user_ids)
    db_session.add(chat)
    db_session.commit()
    db_session.refresh(chat)
    return chat
