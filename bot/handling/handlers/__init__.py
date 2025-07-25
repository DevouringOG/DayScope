from typing import List
from aiogram import Router

from .start import start_router
from .tasks import task_create_handler, task_set_title_handler, task_button_on_click, task_update_value_handler, task_change_title_handler


__all__ = ["task_create_handler", "task_set_title_handler", "task_button_on_click", "task_update_value_handler", "task_change_title_handler"]


def get_routers() -> List[Router]:
    return (
        start_router,
    )
