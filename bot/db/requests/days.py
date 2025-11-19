from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Day


async def orm_get_today_for_user(
    session: AsyncSession,
    user_telegram_id: int,
) -> int:
    """Get or create a Day for today for a user and return its id."""
    today = datetime.today().date()

    stmt = (
        insert(Day)
        .values(
            date=today,
            user=user_telegram_id,
        )
        .on_conflict_do_update(
            index_elements=["user", "date"],
            set_=dict(date=insert(Day).excluded.date),  # No-op update
        )
        .returning(Day.id)
    )

    result = await session.execute(stmt)
    day_id = result.scalar()

    await session.commit()
    return day_id
