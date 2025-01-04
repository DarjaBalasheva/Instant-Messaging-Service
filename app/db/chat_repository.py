from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_model import Chat
from app.models.chat import CreateChatModel


def create_new_chat(chat: CreateChatModel,
                    db_session: AsyncSession,
                    user_ids: int):

    chat = Chat(**chat.dict(), user_ids=user_ids)
    db_session.add(chat)
    db_session.commit()
    db_session.refresh(chat)
    return chat
