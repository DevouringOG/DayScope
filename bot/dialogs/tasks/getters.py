from aiogram_dialog import DialogManager

from bot.db.requests import orm_get_task, orm_get_user_tasks
from bot.utils import get_session


async def task_list_getter(dialog_manager: DialogManager, *args, **kwargs):
    session = get_session(dialog_manager)
    user_telegram_id = dialog_manager.event.from_user.id

    tasks = await orm_get_user_tasks(session, user_telegram_id)
    return {
        "tasks": [{"id": str(task.id), "title": task.title} for task in tasks]
    }


async def current_task_getter(dialog_manager: DialogManager, *args, **kwargs):
    session = get_session(dialog_manager)
    current_task_id = dialog_manager.start_data.get("current_task_id")

    task = await orm_get_task(session, current_task_id)

    dialog_manager.dialog_data.update(
        {"task_title": task.title, "task_value": task.value}
    )

    return {"title": task.title, "value": task.value}
