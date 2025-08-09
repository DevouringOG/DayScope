from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, ListGroup, Cancel, Start, SwitchTo, Back
from bot.handling.custom_widgets import I18NFormat

from bot.handling.states import CreateNote
from bot.handling.handlers import note_text_input, save_note


create_note_dialog = Dialog(
    Window(
        I18NFormat("enter-note-text"),
        MessageInput(
            func=note_text_input,
            content_types=ContentType.TEXT,
        ),
        state=CreateNote.enter_text,
    ),
    Window(
        I18NFormat("confirm-note-text"),
        Cancel(text=I18NFormat("save"), on_click=save_note),
        SwitchTo(
            text=I18NFormat("change-note-text"),
            id="change_text",
            state=CreateNote.edit_text,
        ),
        state=CreateNote.confirm_text,
    ),
    Window(
        I18NFormat("enter-edited-note-text"),
        MessageInput(
            func=note_text_input,
            content_types=ContentType.TEXT,
        ),
        state=CreateNote.edit_text,
    ),
)

current_note_dialog = Dialog(
    Window(
        I18NFormat("note-view"),
        
    )
)