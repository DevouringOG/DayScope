from typing import List

from aiogram_dialog import Dialog

from .notes.dialog import create_note_dialog, current_note_dialog
from .start_menu.dialog import menu_dialog
from .start_menu.first_start_dialog import first_start_dialog
from .tasks.dialog import (
    create_task_dialog,
    tasks_view_dialog,
    view_current_task,
)
from .today.dialog import today_dialog


def get_dialogs() -> List[Dialog]:
    return (
        first_start_dialog,
        create_task_dialog,
        tasks_view_dialog,
        view_current_task,
        menu_dialog,
        today_dialog,
        create_note_dialog,
        current_note_dialog,
    )
