import structlog
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.db.requests import orm_note_remove, orm_note_save
from bot.handling.dialogs.states import CreateNoteSG, TodaySG

logger = structlog.get_logger(__name__)


async def note_text_input(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    note_text = message.text
    dialog_manager.dialog_data["note_text"] = note_text
    await dialog_manager.switch_to(state=CreateNoteSG.confirm_text)


async def save_note(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    note_text = dialog_manager.dialog_data["note_text"]
    day_id = dialog_manager.start_data["day_id"]
    session = dialog_manager.middleware_data["session"]
    await orm_note_save(session, note_text, day_id)


async def note_remove(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    session = dialog_manager.middleware_data["session"]
    day_id = dialog_manager.start_data["day_id"]
    await orm_note_remove(session, day_id)

    i18n = dialog_manager.middleware_data["i18n"]
    await callback.message.edit_text(i18n.note.remove.success())
    await dialog_manager.start(
        state=TodaySG.view, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND
    )
