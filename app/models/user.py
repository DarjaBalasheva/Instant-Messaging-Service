from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# Модель токен-сессии
class Token(BaseModel):
    access_token: str
    token_type: str


# Основная модель пользователя
class UserModel(BaseModel):
    id: UUID
    username: str = Field(max_length=50)
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True  # ORM для работы с SQLAlchemy объектами напрямую


# Модель для регистрации пользователя
class UserRegisterModel(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=3)

    class Config:
        from_attributes = True


# Модель для аутентификации пользователя (вход)
class UserLoginModel(BaseModel):
    username: str
    password: str
