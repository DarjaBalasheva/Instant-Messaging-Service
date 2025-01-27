from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Query,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connect import get_db_session
from app.db.message_repository import get_all_messages_by_chat_id
from app.models.message import MessageModel
from app.models.user import UserModel
from app.models.websocket import ConnectionManager
from app.services.chat_services import get_chat
from app.services.message_services import save_message
from app.services.user_services import get_current_user

router = APIRouter()

manager = ConnectionManager()


# active_connections: dict[UUID, list[WebSocket]] = {}


# Эндпоинт для просмотра сообщения чата
@router.get(
    "/messages", response_model=list[MessageModel], status_code=status.HTTP_200_OK
)
async def get_messages(
    chat_id: UUID,
    db_session: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_user),
):
    chat = await get_chat(
        chat_id=chat_id, user_id=current_user.id, db_session=db_session
    )

    messages = await get_all_messages_by_chat_id(chat_id=chat.id, db_session=db_session)

    return messages


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.websocket("/ws")
async def chat_websocket(
    chat_id: UUID,
    websocket: WebSocket,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
    db_session: AsyncSession = Depends(get_db_session),
):
    try:
        await manager.connect(websocket=websocket)

        while True:
            data = await websocket.receive_text()
            current_user = await get_current_user(
                db_session=db_session, token=cookie_or_token
            )
            chat = await get_chat(
                chat_id=chat_id, user_id=current_user.id, db_session=db_session
            )

            message = await save_message(
                chat_id=chat.id,
                sender_id=current_user.id,
                content=data,
                db_session=db_session,
            )
            await manager.broadcast(message.content)
            # await manager.send_json(f"You wrote: {message}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{current_user.id} left the chat")
    finally:
        await db_session.close() if db_session else None

    # except Exception as e:
    #     print(f"Error: {e}", )
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
