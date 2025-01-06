from fastapi import APIRouter, WebSocket, WebSocketDisconnect,  Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.security import get_decode_userid
from app.db.message_repository import get_all_messages_by_chat_id, save_message_to_db
from app.db.chat_repository import get_chat_by_chat_id
from app.db.db_connect import get_db_session
from app.models.chat import ChatModel
from app.models.message import MessageModel, NewMessageModel

from app.models.user import UserModel
from app.services.chat_services import get_chat
from app.services.message_services import broadcast_message
from app.services.user_services import get_current_user
from datetime import datetime

router = APIRouter()

active_connections: dict[UUID, list[WebSocket]] = {}


# Эндпоинт для просмотра сообщения чата
@router.get("/messages", response_model=list[MessageModel], status_code=status.HTTP_200_OK)
async def get_messages(chat_id: UUID,
                       db_session: AsyncSession = Depends(get_db_session),
                       current_user: UserModel = Depends(get_current_user)
                       ):
    chat = await get_chat(chat_id=chat_id,
                          user_id=current_user.id,
                          db_session=db_session)

    messages = await get_all_messages_by_chat_id(chat_id=chat.id,
                                                 db_session=db_session)

    return messages


@router.websocket("/ws")
async def chat_websocket(chat_id: UUID,
                         websocket: WebSocket,
                         db_session: AsyncSession = Depends(get_db_session)):
    await websocket.accept()
    data = await websocket.receive_json()
    try:
        sender_id = UUID(data.get("sender_id"))
        chat = await get_chat(chat_id=chat_id, user_id=sender_id, db_session=db_session)
    except HTTPException as e:
        print(e)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    if chat.id not in active_connections:
        active_connections[chat.id] = []
    active_connections[chat.id].append(websocket)

    try:
        while True:
            new_message = NewMessageModel(chat_id=chat.id,
                                          sender_id=sender_id,
                                          content=data.get("content"))
            print(new_message)
            message = await save_message_to_db(new_message=new_message,
                                               db_session=db_session)
            await broadcast_message(chat_id=chat_id, message=message, active_connections=active_connections)

    except WebSocketDisconnect:

        # Удаляем соединение при отключении пользователя
        active_connections[chat_id].remove(websocket)

        if not active_connections[chat_id]:
            del active_connections[chat_id]

    except Exception as e:
        print(f"Error: {e}",)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    finally:
        await db_session.close()
