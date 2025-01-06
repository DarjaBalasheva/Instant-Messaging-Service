import json
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import get_decode_userid, oauth2_scheme
from app.db.db_connect import get_db_session
from app.db.db_model import User
from app.db.user_repository import create_user_in_db, get_user_by_username
from app.models.message import MessageModel
from app.models.user import UserRegisterModel, UserLoginModel, UserModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext


async def broadcast_message(chat_id: UUID, message: MessageModel, active_connections: dict):
    message_data = message.dict()

    # TODO: Наладить автоматическое преобразование в строку через Pydantic
    message_data['id'] = str(message_data['id'])
    message_data['chat_id'] = str(message_data['chat_id'])
    message_data['sender_id'] = str(message_data['sender_id'])
    message_data['timestamp'] = message_data['timestamp'].isoformat()

    if chat_id in active_connections:
        for connection in active_connections[chat_id]:
            try:
                await connection.send_json(message_data)
            except RuntimeError:
                print("runtime error")
                active_connections[chat_id].remove(connection)
                if not active_connections[chat_id]:
                    del active_connections[chat_id]
