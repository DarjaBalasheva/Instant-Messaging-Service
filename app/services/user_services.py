from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import get_decode_userid, oauth2_scheme
from app.db.db_connect import get_db_session
from app.db.db_model import User
from app.db.user_repository import create_user_in_db, get_user_by_username
from app.models.user import UserRegisterModel, UserLoginModel, UserModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user: UserRegisterModel, db_session: AsyncSession) -> UserModel:
    # Проверка никнейма в базе
    existing_user = await get_user_by_username(user=user, db_session=db_session)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = await create_user_in_db(user=user, db_session=db_session)

    return new_user


async def login_user(user_login: UserLoginModel, db_session: AsyncSession) -> User:
    user = await get_user_by_username(user=user_login, db_session=db_session)

    # Проверка наличия пользователя и статус аккаунта
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is inactive")

    # Проверка пароля
    if not pwd_context.verify(user_login.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return user


async def get_current_user(db_session: AsyncSession = Depends(get_db_session), token: str = Depends(oauth2_scheme)):
    user_id = get_decode_userid(token=token)
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
