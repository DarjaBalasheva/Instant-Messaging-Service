from fastapi import APIRouter

from app.apis.v1 import user_routes, chat_routes

api_router = APIRouter()
api_router.include_router(user_routes.router, prefix="", tags=["users"])
api_router.include_router(chat_routes.router, prefix="", tags=["chats"])
