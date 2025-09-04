from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Day, Note, Task, TaskStatus, User


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


async def orm_add_task(
    session: AsyncSession,
    user_telegram_id: int,
    title: str,
    value: int,
) -> None:
    """Create a Task for a user."""
    stmt = insert(Task).values(
        {
            "title": title,
            "value": value,
            "user": user_telegram_id,
        },
    )

    await session.execute(stmt)
    await session.commit()


async def orm_get_user_tasks(
    session: AsyncSession,
    user_telegram_id: int,
) -> List[Task]:
    """Return all tasks for a given user."""
    stmt = select(Task).where(Task.user == user_telegram_id)
    response = await session.scalars(stmt)
    return response.all()


async def orm_get_task(
    session: AsyncSession,
    task_id: int,
) -> Optional[Task]:
    """Return a single Task by id or None if not found."""
    stmt = select(Task).where(Task.id == task_id)
    response = await session.scalar(stmt)
    return response


async def orm_task_update_value(
    session: AsyncSession,
    task_id: int,
    value: int,
) -> None:
    """Update value of a task."""
    stmt = update(Task).where(Task.id == task_id).values(value=value)
    await session.execute(stmt)
    await session.commit()


async def orm_task_change_title(
    session: AsyncSession,
    task_id: int,
    new_title: str,
) -> None:
    """Change title of a task."""
    stmt = update(Task).where(Task.id == task_id).values(title=new_title)
    await session.execute(stmt)
    await session.commit()


async def orm_task_remove(
    session: AsyncSession,
    task_id: int,
) -> None:
    """Remove task by id."""
    stmt = delete(Task).where(Task.id == task_id)
    await session.execute(stmt)
    await session.commit()


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


async def orm_get_tasks_statuses(
    session: AsyncSession,
    day_id: int,
    user_telegram_id: int,
) -> List[Tuple[TaskStatus, Task]]:  # Need refactor
    """
    Return list of (TaskStatus, Task) tuples for the given day.
    If TaskStatus rows are missing for some user tasks, create them.
    """
    stmt = (
        select(TaskStatus, Task)
        .join(Task, TaskStatus.task == Task.id)
        .where(TaskStatus.day == day_id)
        .order_by(TaskStatus.id)
    )
    user_tasks = await orm_get_user_tasks(session, user_telegram_id)
    response = await session.execute(stmt)
    task_statuses_with_tasks = response.all()

    if len(task_statuses_with_tasks) < len(user_tasks):
        for task in user_tasks:
            stmt = (
                insert(TaskStatus)
                .values(task=task.id, day=day_id, completed=False)
                .on_conflict_do_nothing()
            )
            await session.execute(stmt)
        await session.commit()

        stmt = (
            select(TaskStatus, Task)
            .join(Task, TaskStatus.task == Task.id)
            .where(TaskStatus.day == day_id)
            .order_by(TaskStatus.id)
        )
        response = await session.execute(stmt)
        task_statuses_with_tasks = response.all()

    return task_statuses_with_tasks


async def orm_task_change_status(
    session: AsyncSession,
    task_id: int,
) -> None:
    """Toggle completed flag on TaskStatus row by id."""
    stmt = (
        update(TaskStatus)
        .where(TaskStatus.id == task_id)
        .values(completed=~TaskStatus.completed)
    )
    await session.execute(stmt)
    await session.commit()


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
