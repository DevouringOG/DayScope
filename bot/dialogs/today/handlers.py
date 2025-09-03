import structlog
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, SubManager
from aiogram_dialog.widgets.kbd import Button, Start

from bot.db.requests import orm_task_change_status
from bot.dialogs.states import CreateNoteSG, CurrentNoteSG

logger = structlog.get_logger(__name__)


async def check_task_button_on_click_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: SubManager,
) -> None:
    """Toggle a task status when its button is clicked."""
    task_id = dialog_manager.item_id
    session = dialog_manager.middleware_data["session"]
    await orm_task_change_status(session, int(task_id))


async def create_note_on_click_handler(
    callback: CallbackQuery,
    button: Start,
    dialog_manager: DialogManager,
) -> None:
    """Start create note dialog with provided 'day_id'."""
    await dialog_manager.start(
        state=CreateNoteSG.enter_text,
        data={
            "day_id": int(dialog_manager.dialog_data["today_id"]),
        },
    )


async def view_note_on_click_handler(
    callback: CallbackQuery,
    button: Start,
    dialog_manager: DialogManager,
) -> None:
    """Open existing note view dialog with note text in start data."""
    await dialog_manager.start(
        state=CurrentNoteSG.view,
        data={
            "day_id": int(dialog_manager.dialog_data["today_id"]),
            "note_text": dialog_manager.dialog_data["note_text"],
        },
    )
