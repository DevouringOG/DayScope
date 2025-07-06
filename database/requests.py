from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from database.models import User


async def orm_add_user(
        session: AsyncSession,
        telegram_id: int,
        lang: str,
):
    stmt = insert(User).values(
        {
            "telegram_id": telegram_id,
            "lang": lang,
        },
    ).on_conflict_do_nothing(index_elements=["telegram_id"])

    await session.execute(stmt)
    await session.commit()


async def orm_get_user_by_id(
        session: AsyncSession,
        telegram_id: int,
):
    stmt = select(User).where(User.telegram_id == telegram_id)
    response = await session.scalar(stmt)
    return response
