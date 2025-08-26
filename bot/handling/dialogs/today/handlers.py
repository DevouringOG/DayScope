import structlog
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, SubManager
from aiogram_dialog.widgets.kbd import Button, Start

from bot.db.requests import orm_task_change_status
from bot.handling.dialogs.states import CreateNoteSG, CurrentNoteSG

logger = structlog.get_logger(__name__)


async def check_task_button_on_click(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: SubManager,
):
    task_id = dialog_manager.item_id
    session = dialog_manager.middleware_data["session"]
    await orm_task_change_status(session, int(task_id))


async def create_note_on_click(
    callback: CallbackQuery,
    button: Start,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(
        state=CreateNoteSG.enter_text,
        data={
            "day_id": int(dialog_manager.dialog_data["today_id"]),
        },
    )


async def view_note_on_click(
    callback: CallbackQuery,
    button: Start,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(
        state=CurrentNoteSG.view,
        data={
            "day_id": int(dialog_manager.dialog_data["today_id"]),
            "note": int(dialog_manager.dialog_data["note"]),
        },
    )
