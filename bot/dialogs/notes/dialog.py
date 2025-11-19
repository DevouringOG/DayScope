from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, SwitchTo

from bot.custom_widgets import I18nFormat
from bot.dialogs.notes.getters import note_view_getter
from bot.dialogs.notes.handlers import (
    note_change_text_input_handler,
    note_remove_handler,
    note_save_handler,
    note_text_input_handler,
)
from bot.dialogs.states import CreateNoteSG, CurrentNoteSG

create_note_dialog = Dialog(
    Window(
        I18nFormat("enter-note-text"),
        MessageInput(
            func=note_text_input_handler, content_types=ContentType.TEXT
        ),
        state=CreateNoteSG.enter_text,
    ),
    Window(
        I18nFormat("confirm-note-text"),
        Cancel(text=I18nFormat("save"), on_click=note_save_handler),
        SwitchTo(
            text=I18nFormat("change-note-text"),
            id="change_text",
            state=CreateNoteSG.edit_text,
        ),
        state=CreateNoteSG.confirm_text,
    ),
    Window(
        I18nFormat("enter-edited-note-text"),
        MessageInput(
            func=note_text_input_handler, content_types=ContentType.TEXT
        ),
        state=CreateNoteSG.edit_text,
    ),
)

current_note_dialog = Dialog(
    Window(
        I18nFormat("note-view"),
        Cancel(text=I18nFormat("back")),
        SwitchTo(
            text=I18nFormat("change-note-text"),
            id="to_change_note_text",
            state=CurrentNoteSG.change_text,
        ),
        SwitchTo(
            text=I18nFormat("remove"),
            id="to_remove_note",
            state=CurrentNoteSG.confirm_remove,
        ),
        getter=note_view_getter,
        state=CurrentNoteSG.view,
    ),
    Window(
        I18nFormat("note-confirm-remove"),
        Row(
            Button(
                text=I18nFormat("remove"),
                on_click=note_remove_handler,
                id="btn_note_remove_confirm",
            ),
            SwitchTo(
                text=I18nFormat("back"),
                state=CurrentNoteSG.view,
                id="btn_back_to_note_view",
            ),
        ),
        state=CurrentNoteSG.confirm_remove,
    ),
    Window(
        I18nFormat("enter-edited-note-text"),
        MessageInput(
            func=note_change_text_input_handler, content_types=ContentType.TEXT
        ),
        state=CurrentNoteSG.change_text,
    ),
)
