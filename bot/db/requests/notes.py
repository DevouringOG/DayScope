from typing import Optional

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Note


async def orm_note_save(
    session: AsyncSession,
    note_text: str,
    day_id: int,
) -> None:
    """Create a note for a day."""
    stmt = insert(Note).values(
        day=day_id,
        text=note_text,
    )
    await session.execute(stmt)
    await session.commit()


async def orm_get_note(
    session: AsyncSession,
    day_id: int,
) -> Optional[str]:
    """Return the text of a note for a day or None if not present."""
    stmt = select(Note.text).where(Note.day == day_id)
    response = await session.execute(stmt)
    note = response.scalar()
    return note


async def orm_note_remove(
    session: AsyncSession,
    day_id: int,
) -> None:
    """Remove a note for a given day."""
    stmt = delete(Note).where(Note.day == day_id)
    await session.execute(stmt)
    await session.commit()


async def orm_note_change_text(
    session: AsyncSession,
    day_id: int,
    new_text: str,
) -> None:
    """Change text of a note."""
    stmt = update(Note).where(Note.day == day_id).values(text=new_text)
    await session.execute(stmt)
    await session.commit()
