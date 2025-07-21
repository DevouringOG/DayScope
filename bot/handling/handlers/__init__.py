from typing import List
from aiogram import Router

from .start import start_router
from .tasks import task_set_value_handler, task_set_title_handler, task_button_on_click


__all__ = ["task_set_value_handler", "task_set_title_handler", "task_button_on_click"]


def get_routers() -> List[Router]:
    return (
        start_router,
    )
