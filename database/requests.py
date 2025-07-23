from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
from database.models import User, Task


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
