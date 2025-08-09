from typing import List
from aiogram import Router

from .start import start_router
from .tasks import task_create_handler, task_set_title_handler, task_button_on_click, task_update_value_handler, task_change_title_handler, task_remove
from .today import check_task_button_on_click, to_create_note_onclick
from .note import note_text_input, save_note


__all__ = [
    "start_router",
    "task_create_handler",
    "task_set_title_handler",
    "task_button_on_click",
    "task_update_value_handler",
    "task_change_title_handler",
    "task_remove",
    "check_task_button_on_click",
    "note_text_input",
    "save_note",
    "note_text_input",
    "save_note",
    "to_create_note_onclick",
]


def get_routers() -> List[Router]:
    return (
        start_router,
    )
