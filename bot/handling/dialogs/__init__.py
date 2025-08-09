from typing import List
from aiogram_dialog import Dialog

from .first_start import first_start_dialog
from .tasks import create_task_dialog, view_tasks_dialog, view_current_task
from .menu import menu_dialog
from .today import today_dialog
from .note import create_note_dialog


def get_dialogs() -> List[Dialog]:
    return (
        first_start_dialog,
        create_task_dialog,
        view_tasks_dialog,
        view_current_task,
        menu_dialog,
        today_dialog,
        create_note_dialog,
    )
