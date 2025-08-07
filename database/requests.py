from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, delete
from database.models import User, Task, TaskStatus, Day
import structlog


logger = structlog.get_logger(__name__)


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
    ).on_conflict_do_nothing(
        index_elements=["telegram_id"]
    ).returning(User.telegram_id)

    result = await session.execute(stmt)
    await session.commit()
    return result.scalar() is not None


async def orm_get_user_by_id(
        session: AsyncSession,
        telegram_id: int,
):
    stmt = select(User).where(User.telegram_id == telegram_id)
    response = await session.scalar(stmt)
    return response


async def orm_add_task(
        session: AsyncSession,
        user_telegram_id: int,
        title: str,
        value: int,
):
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
):
    stmt = select(Task).where(Task.user == user_telegram_id)
    response = await session.scalars(stmt)
    return response.all()


async def orm_get_task(
        session: AsyncSession,
        task_id: int,
):
    stmt = select(Task).where(Task.id == task_id)
    response = await session.scalar(stmt)
    return response


async def orm_task_update_value(
        session: AsyncSession,
        task_id: int,
        value: int,
):
    stmt = update(Task).where(Task.id == task_id).values(value=value)
    await session.execute(stmt)
    await session.commit()


async def orm_task_change_title(
        session: AsyncSession,
        task_id: int,
        new_title: str,        
):
    stmt = update(Task).where(Task.id == task_id).values(title=new_title)
    await session.execute(stmt)
    await session.commit()


async def orm_task_remove(
        session: AsyncSession,
        task_id: int,
):
    stmt = delete(Task).where(Task.id == task_id)
    await session.execute(stmt)
    await session.commit()


async def orm_get_today_for_user(
        session: AsyncSession,
        user_telegram_id: int,
):
    today = datetime.today().date()
    
    stmt = insert(Day).values(
        date=today,
        user=user_telegram_id,
    ).on_conflict_do_update(
        index_elements=["user", "date"],
        set_=dict(date=insert(Day).excluded.date)  # No-op update
    ).returning(Day.id)

    result = await session.execute(stmt)
    day_id = result.scalar()
    
    await session.commit()
    return day_id


async def orm_get_tasks_statuses(
        session: AsyncSession,
        day_id: int,
        user_telegram_id: int,
):
    logger.info("DAY ID", day_id=day_id)
    # Join TaskStatus with Task to get task details
    stmt = select(TaskStatus, Task).join(Task, TaskStatus.task == Task.id).where(TaskStatus.day == day_id).order_by(TaskStatus.id)
    user_tasks = await orm_get_user_tasks(session, user_telegram_id)
    response = await session.execute(stmt)
    task_statuses_with_tasks = response.all()
    logger.info("Response", response=task_statuses_with_tasks)
    
    if len(task_statuses_with_tasks) < len(user_tasks):
        for task in user_tasks:
            stmt = insert(TaskStatus).values(
                task=task.id,
                day=day_id,
                completed=False
            ).on_conflict_do_nothing()
            await session.execute(stmt)
        await session.commit()
        
        # Re-fetch with join after inserting new records
        stmt = select(TaskStatus, Task).join(Task, TaskStatus.task == Task.id).where(TaskStatus.day == day_id).order_by(TaskStatus.id)
        response = await session.execute(stmt)
        task_statuses_with_tasks = response.all()
    
    return task_statuses_with_tasks


async def orm_task_change_status(
        session: AsyncSession,
        task_id: int,
):
    stmt = update(TaskStatus).where(TaskStatus.id == task_id).values(completed=~TaskStatus.completed)
    await session.execute(stmt)
    await session.commit()
