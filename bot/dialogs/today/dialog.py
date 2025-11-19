from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, ListGroup, Row, Start
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from bot.custom_widgets import I18nFormat
from bot.dialogs.states import MenuSG, TodaySG
from bot.dialogs.today.getters import today_task_statuses_getter
from bot.dialogs.today.handlers import (
    check_task_button_handler,
    to_create_note_handler,
    to_view_note_handler,
)

today_dialog = Dialog(
    Window(
        I18nFormat("today-text"),
        ListGroup(
            Button(
                text=Format("{item[title]}"),
                id="btn_task",
                on_click=check_task_button_handler,
            ),
            id="tasks_list",
            item_id_getter=lambda x: x["task_status_id"],
            items="tasks",
        ),
        Row(
            Start(
                text=I18nFormat("to-menu"),
                id="btn_start_to_menu",
                state=MenuSG.view,
                mode=StartMode.RESET_STACK,
            ),
            Button(
                text=I18nFormat("create-note"),
                id="btn_to_create_note",
                on_click=to_create_note_handler,
                when=~F["note_exists"],
            ),
            Button(
                text=I18nFormat("view-note"),
                id="btn_to_view_note",
                on_click=to_view_note_handler,
                when=F["note_exists"],
            ),
        ),
        getter=today_task_statuses_getter,
        state=TodaySG.view,
    ),
)
