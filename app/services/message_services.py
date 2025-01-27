from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.message_repository import save_message_to_db
from app.models.message import MessageModel, NewMessageModel


async def save_message(
    chat_id: UUID, sender_id: UUID, content: str, db_session: AsyncSession
) -> MessageModel:
    new_message = NewMessageModel(chat_id=chat_id, sender_id=sender_id, content=content)

    message = await save_message_to_db(new_message=new_message, db_session=db_session)

    return message
