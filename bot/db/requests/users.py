from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


async def orm_add_user(
    session: AsyncSession,
    telegram_id: int,
    lang: str,
) -> bool:
    """
    Insert a user if not exists.
    Returns True if a new user was inserted, False if already existed.
    """
    stmt = (
        insert(User)
        .values(
            {
                "telegram_id": telegram_id,
                "lang": lang,
            },
        )
        .on_conflict_do_nothing(index_elements=["telegram_id"])
        .returning(User.telegram_id)
    )

    result = await session.execute(stmt)
    await session.commit()
    return result.scalar() is not None


async def orm_get_user_by_id(
    session: AsyncSession,
    telegram_id: int,
) -> Optional[User]:
    """Return a User by telegram_id or None if not found."""
    stmt = select(User).where(User.telegram_id == telegram_id)
    response = await session.scalar(stmt)
    return response
