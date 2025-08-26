from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, ListGroup
from aiogram_dialog.widgets.text import Format

from bot.handling.custom_widgets import I18NFormat
from bot.handling.dialogs.states import TodaySG
from bot.handling.dialogs.today.getters import today_task_statuses_list_getter
from bot.handling.dialogs.today.handlers import (
    check_task_button_on_click,
    create_note_on_click,
    view_note_on_click,
)

today_dialog = Dialog(
    Window(
        I18NFormat("today-text"),
        ListGroup(
            Button(
                text=Format("{item[title]}"),
                id="btn_task",
                on_click=check_task_button_on_click,
            ),
            id="tasks_list",
            item_id_getter=lambda x: x["task_status_id"],
            items="tasks",
        ),
        Button(
            text=I18NFormat("create-note"),
            id="btn_to_create_note",
            on_click=create_note_on_click,
        ),
        Button(
            text=I18NFormat("view_note"),
            id="btn_to_view_note",
            on_click=view_note_on_click,
        ),
        Cancel(text=I18NFormat("back")),
        getter=today_task_statuses_list_getter,
        state=TodaySG.view,
    ),
)
