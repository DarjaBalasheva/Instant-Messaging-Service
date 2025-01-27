from fastapi import APIRouter

from app.apis.v1 import chat_routes, message_routes, user_routes

api_router = APIRouter()
api_router.include_router(user_routes.router, prefix="", tags=["users"])
api_router.include_router(chat_routes.router, prefix="", tags=["chats"])
api_router.include_router(
    message_routes.router, prefix="/chats/{chat_id}", tags=["messages"]
)

# Регистрация WebSocket маршрута
api_router.add_api_websocket_route(
    path="/chats/{chat_id}/ws",
    endpoint=message_routes.chat_websocket,
    name="chat_websocket",
)
