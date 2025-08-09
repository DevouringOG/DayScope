from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, SubManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Start
from fluentogram import TranslatorRunner
import structlog

from bot.handling.states import CreateNote
from database.requests import orm_task_change_status


logger = structlog.get_logger(__name__)


async def check_task_button_on_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: SubManager,
):
    task_id = dialog_manager.item_id
    session = dialog_manager.middleware_data["session"]
    await orm_task_change_status(session, int(task_id))


async def to_create_note_onclick(
        callback: CallbackQuery,
        button: Start,
        dialog_manager: DialogManager,
):
    """Navigate to the selected task's detailed view."""
    await dialog_manager.start(
        state=CreateNote.enter_text,
        data={
            "day_id": int(dialog_manager.dialog_data["today_id"]),
        },
    )
