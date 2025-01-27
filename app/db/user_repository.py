from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_model import User
from app.models.user import UserModel


async def get_user_by_username(user, db_session: AsyncSession) -> User | None:
    stmt = select(User).filter(User.username == user.username)
    result = await db_session.execute(stmt)
    existing_user = result.scalars().first()
    return existing_user


async def get_user_by_user_id(
    user_id: UUID, db_session: AsyncSession
) -> UserModel | None:
    stmt = select(User).filter(User.id == user_id)
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    return UserModel.from_orm(user)


async def create_user_in_db(user, db_session: AsyncSession) -> UserModel:
    new_user = User(
        email=user.email, username=user.username, password_hash=user.password
    )
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    return UserModel.from_orm(new_user)
