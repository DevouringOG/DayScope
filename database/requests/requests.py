from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from database.models import User


async def add_user(
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
