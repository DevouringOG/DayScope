from aiogram_dialog import DialogManager
import structlog

from database.requests import orm_get_user_tasks, orm_get_task, orm_get_tasks_statuses, orm_get_today_for_user


logger = structlog.get_logger(__name__)


async def task_list_getter(dialog_manager: DialogManager, *args, **kwargs):
    session = dialog_manager.middleware_data["session"]
    user_telegram_id = dialog_manager.event.from_user.id
    
    tasks = await orm_get_user_tasks(session, user_telegram_id)
    return {
        "tasks": [
            {"id": str(task.id), "title": task.title}
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


async def today_task_statuses_list_getter(dialog_manager: DialogManager, *args, **kwargs):
    session = dialog_manager.middleware_data["session"]
    user_telegram_id = dialog_manager.event.from_user.id

    today_id = await orm_get_today_for_user(session, user_telegram_id)
    dialog_manager.dialog_data["today_id"] = today_id
    
    tasks_statuses_with_tasks = await orm_get_tasks_statuses(session, today_id, user_telegram_id)
    
    # Check if note exists for today (you'll need to implement orm_get_note_for_today)
    # note_exists = await orm_get_note_for_today(session, today_id, user_telegram_id) is not None
    note_exists = True  # Placeholder - replace with actual database check
    
    ret_data = {
        "tasks": [
            {
                "task_status_id": str(task_status.id),
                "title": task.title + (" ✅" if task_status.completed else " ⭕"),
            }
            for task_status, task in tasks_statuses_with_tasks
        ],
        "note_exists": note_exists,
        "today_id": today_id,
    }
    logger.info("DATA", tasks_statuses=tasks_statuses_with_tasks)
    return ret_data
