from fastapi import APIRouter, WebSocket, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.security import get_decode_userid
from app.db.chat_repository import create_new_chat, get_all_chats_by_user_id
from app.db.db_connect import get_db_session
from app.models.chat import CreateChatModel, ChatModel

from app.models.user import UserModel
from app.services.user_services import get_current_user
from datetime import datetime

router = APIRouter()


# Эндпоинт для просмотра чатов пользователя
@router.get("/chats", response_model=list[ChatModel], status_code=status.HTTP_200_OK)
async def get_chats(db_session: AsyncSession = Depends(get_db_session),
                    current_user: UserModel = Depends(get_current_user)):
    chats = await get_all_chats_by_user_id(db_session=db_session,
                                           user_id=current_user.id)

    return chats


# Эндпоинт для создания нового чата
@router.post("/chats", response_model=ChatModel, status_code=status.HTTP_201_CREATED)
async def create_chat(chat: CreateChatModel,
                      db_session: AsyncSession = Depends(get_db_session),
                      current_user: UserModel = Depends(get_current_user)):
    new_chat = create_new_chat(chat=chat,
                               db_session=db_session,
                               user_ids=[current_user.id])
    return new_chat
