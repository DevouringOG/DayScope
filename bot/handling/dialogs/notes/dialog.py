from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row, SwitchTo

from bot.handling.custom_widgets import I18NFormat
from bot.handling.dialogs.notes.handlers import (
    note_remove,
    note_text_input,
    save_note,
)
from bot.handling.dialogs.states import CreateNoteSG, CurrentNoteSG

create_note_dialog = Dialog(
    Window(
        I18NFormat("enter-note-text"),
        MessageInput(func=note_text_input, content_types=ContentType.TEXT),
        state=CreateNoteSG.enter_text,
    ),
    Window(
        I18NFormat("confirm-note-text"),
        Cancel(text=I18NFormat("save"), on_click=save_note),
        SwitchTo(
            text=I18NFormat("change-note-text"),
            id="change_text",
            state=CreateNoteSG.edit_text,
        ),
        state=CreateNoteSG.confirm_text,
    ),
    Window(
        I18NFormat("enter-edited-note-text"),
        MessageInput(func=note_text_input, content_types=ContentType.TEXT),
        state=CreateNoteSG.edit_text,
    ),
)

current_note_dialog = Dialog(
    Window(
        I18NFormat("note-view"),
        Back(text=I18NFormat("back")),
        SwitchTo(
            text=I18NFormat("change-note-text"),
            id="to_change_note_text",
            state=CurrentNoteSG.change_text,
        ),
        SwitchTo(
            text=I18NFormat("remove"),
            id="to_remove_note",
            state=CurrentNoteSG.confirm_remove,
        ),
        state=CurrentNoteSG.view,
    ),
    Window(
        I18NFormat("note-confirm-remove"),
        Row(
            Button(
                text=I18NFormat("remove"),
                on_click=note_remove,
                id="btn_note_remove_confirm",
            ),
            SwitchTo(
                text=I18NFormat("back"),
                state=CurrentNoteSG.view,
                id="btn_back_to_note_view",
            ),
        ),
        state=CurrentNoteSG.confirm_remove,
    ),
)
