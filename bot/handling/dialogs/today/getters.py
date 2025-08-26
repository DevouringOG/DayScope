import structlog
from aiogram_dialog import DialogManager

from bot.db.requests import (
    orm_get_note,
    orm_get_tasks_statuses,
    orm_get_today_for_user,
)

logger = structlog.get_logger(__name__)


async def today_task_statuses_list_getter(
    dialog_manager: DialogManager, *args, **kwargs
):
    session = dialog_manager.middleware_data["session"]
    user_telegram_id = dialog_manager.event.from_user.id

    today_id = await orm_get_today_for_user(session, user_telegram_id)
    dialog_manager.dialog_data["today_id"] = today_id

    tasks_statuses_with_tasks = await orm_get_tasks_statuses(
        session, today_id, user_telegram_id
    )

    note = await orm_get_note(session, today_id)
    dialog_manager.dialog_data["note"] = note
    logger.info("NOTE EXISTS", note=note)

    ret_data = {
        "tasks": [
            {
                "task_status_id": str(task_status.id),
                "title": task.title
                + (" ✅" if task_status.completed else " ⭕"),
            }
            for task_status, task in tasks_statuses_with_tasks
        ],
        "note": note,
        "today_id": today_id,
    }
    logger.info("DATA", tasks_statuses=tasks_statuses_with_tasks)
    return ret_data
