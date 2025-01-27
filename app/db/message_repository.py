from typing import Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_model import Message
from app.models.message import MessageModel, NewMessageModel


async def get_all_messages_by_chat_id(
    chat_id: UUID, db_session: AsyncSession
) -> Sequence[Message]:
    stmt = select(Message).where(Message.chat_id == chat_id)
    result = await db_session.execute(stmt)
    messages = result.scalars().all()
    return messages


async def save_message_to_db(
    new_message: NewMessageModel, db_session: AsyncSession
) -> MessageModel:
    message = Message(**new_message.dict())

    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    await db_session.close()

    return MessageModel.from_orm(message)
