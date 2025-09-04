from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.db.requests import (
    orm_note_change_text,
    orm_note_remove,
    orm_note_save,
)
from bot.dialogs.states import CreateNoteSG, CurrentNoteSG, TodaySG
from bot.utils import get_i18n, get_session


async def note_text_input_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """Store entered note text and move to confirmation step."""
    note_text = message.text
    dialog_manager.dialog_data["note_text"] = note_text
    await dialog_manager.switch_to(state=CreateNoteSG.confirm_text)


async def note_save_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    """Persist note text for the current day."""
    note_text = dialog_manager.dialog_data.get("note_text", "")
    day_id = dialog_manager.start_data.get("day_id")

    session = get_session(dialog_manager)
    await orm_note_save(session, note_text, day_id)


async def note_remove_handler(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    """Remove note for the day and return to Today view."""
    session = get_session(dialog_manager)
    day_id = dialog_manager.start_data.get("day_id")

    await orm_note_remove(session, day_id)

    i18n = get_i18n(dialog_manager)
    await callback.message.edit_text(i18n.note.remove.success())
    await dialog_manager.start(
        state=TodaySG.view, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND
    )


async def note_change_text_input_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """Save edited note text into DB and switch to view state."""
    new_note_text = message.text
    dialog_manager.dialog_data["note_text"] = new_note_text

    session = get_session(dialog_manager)
    await orm_note_change_text(
        session, dialog_manager.start_data["day_id"], new_note_text
    )

    await dialog_manager.switch_to(state=CurrentNoteSG.view)
