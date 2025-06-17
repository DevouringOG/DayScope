from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from database.models import User


async def upsert_user(
        session: AsyncSession,
        telegram_id: int,
        first_name: str,
        last_name: str | None = None,
):
    stmt = insert(User).values(
        {
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    stmt.on_conflict_do_update(
        index_elements=["telegram_id"],
        set_={
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    await session.execute(stmt)
    await session.commit()
