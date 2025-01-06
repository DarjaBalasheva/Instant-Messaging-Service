from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import get_decode_userid, oauth2_scheme
from app.db.chat_repository import get_chat_by_chat_id
from app.db.db_connect import get_db_session
from app.db.db_model import User, Chat
from app.db.user_repository import create_user_in_db, get_user_by_username
from app.models.user import UserRegisterModel, UserLoginModel, UserModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext


async def get_chat(chat_id: UUID,
                   user_id: UUID,
                   db_session: AsyncSession) -> Chat:
    chat = await get_chat_by_chat_id(chat_id=chat_id, db_session=db_session)
    if not chat:
        raise HTTPException(status_code=400, detail="Chat not found")
    print(user_id not in chat.user_ids)
    if user_id not in chat.user_ids:
        raise HTTPException(status_code=403, detail="Permission denied")

    return chat

