from typing import List
from aiogram_dialog import Dialog

from .first_start import first_start_dialog
from .tasks import create_task_dialog


def get_dialogs() -> List[Dialog]:
    return (
        first_start_dialog,
        create_task_dialog,
    )
