from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.chat_repository import (
    create_new_chat,
    get_all_chats_by_user_id,
    update_user_in_chat,
)
from app.db.db_connect import get_db_session
from app.models.chat import ChatModel, CreateChatModel, UsersInChatModel
from app.models.user import UserModel
from app.services.chat_services import get_chat
from app.services.user_services import get_current_user

router = APIRouter()


# Эндпоинт для просмотра чатов пользователя
@router.get("/chats", response_model=list[ChatModel], status_code=status.HTTP_200_OK)
async def get_chats(
    db_session: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    chats = await get_all_chats_by_user_id(
        db_session=db_session, user_id=current_user.id
    )

    return chats


# Эндпоинт для создания нового чата
@router.post("/chats", response_model=ChatModel, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat: CreateChatModel,
    db_session: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    new_chat = create_new_chat(
        chat=chat, db_session=db_session, user_ids=[current_user.id]
    )
    return new_chat


# Эндпоинт для создания нового чата
@router.put("/chats", response_model=ChatModel, status_code=status.HTTP_201_CREATED)
async def create_chat(  # noqa
    data: UsersInChatModel,
    db_session: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    chat = await get_chat(
        chat_id=data.chat_id,
        db_session=db_session,
        user_id=current_user.id,
        check_permission=False,
    )

    if data.is_add and current_user.id not in chat.user_ids:
        chat.user_ids.append(current_user.id)
    elif not data.is_add and current_user.id in chat.user_ids:
        chat.user_ids.remove(current_user.id)

    new_chat = await update_user_in_chat(data=chat, db_session=db_session)
    return new_chat
