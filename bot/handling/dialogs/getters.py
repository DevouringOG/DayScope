from aiogram_dialog import DialogManager

from database.requests import orm_get_user_tasks, orm_get_task


async def get_tasks_getter(dialog_manager: DialogManager, *args, **kwargs):
    session = dialog_manager.middleware_data["session"]
    user_telegram_id = dialog_manager.event.from_user.id
    tasks = await orm_get_user_tasks(session, user_telegram_id)
    return {
        "tasks": [
            {"id": task.id, "title": task.title}
            for task in tasks
        ]
    }


async def current_task_getter(dialog_manager: DialogManager, *args, **kwargs):
    session = dialog_manager.middleware_data["session"]
    current_task_id = dialog_manager.start_data["current_task_id"]
    task = await orm_get_task(session, current_task_id)
    dialog_manager.dialog_data["task_title"] = task.title
    dialog_manager.dialog_data["task_value"] = task.value
    return {
        "title": task.title,
        "value": task.value,
    }
