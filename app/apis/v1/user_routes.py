from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
from app.core.security import create_access_token

from app.db.db_connect import get_db_session
from app.models.user import UserRegisterModel, UserLoginModel, Token, UserModel
from app.services.user_services import create_user, login_user
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


router = APIRouter()


# регистрация пользователя
@router.post("/register", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegisterModel, db_session: AsyncSession = Depends(get_db_session)):
    try:
        user.password = Hasher().get_password_hash(password=user.password)  # Хэширование пароля
        new_user = await create_user(user=user, db_session=db_session)
        return new_user
    except HTTPException as e:
        raise e


@router.post("/login", response_model=Token)
async def login(user_login: UserLoginModel, db_session: AsyncSession = Depends(get_db_session)):
    try:
        user = await login_user(user_login=user_login, db_session=db_session)

        # Создание токена
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
