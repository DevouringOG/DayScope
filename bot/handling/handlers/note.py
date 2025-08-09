from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode, SubManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from fluentogram import TranslatorRunner
import structlog

from bot.handling.states import CreateNote
from database.requests import orm_note_save


logger = structlog.get_logger(__name__)


async def note_text_input(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    note_text = message.text
    dialog_manager.dialog_data["note_text"] = note_text
    await dialog_manager.switch_to(state=CreateNote.confirm_text)


async def save_note(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    note_text = dialog_manager.dialog_data["note_text"]
    day_id = dialog_manager.start_data["day_id"]
    logger.info("TEXT, DAY", text=note_text, day_id=day_id)
