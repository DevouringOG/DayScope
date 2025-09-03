from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, ListGroup, Start
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from bot.custom_widgets import I18nFormat
from bot.dialogs.states import MenuSG, TodaySG
from bot.dialogs.today.getters import today_task_statuses_list_getter
from bot.dialogs.today.handlers import (
    check_task_button_on_click_handler,
    create_note_on_click_handler,
    view_note_on_click_handler,
)

today_dialog = Dialog(
    Window(
        I18nFormat("today-text"),
        ListGroup(
            Button(
                text=Format("{item[title]}"),
                id="btn_task",
                on_click=check_task_button_on_click_handler,
            ),
            id="tasks_list",
            item_id_getter=lambda x: x["task_status_id"],
            items="tasks",
        ),
        Button(
            text=I18nFormat("create-note"),
            id="btn_to_create_note",
            on_click=create_note_on_click_handler,
            when=~F["note_exists"],
        ),
        Button(
            text=I18nFormat("view-note"),
            id="btn_to_view_note",
            on_click=view_note_on_click_handler,
            when=F["note_exists"],
        ),
        Start(
            text=I18nFormat("to-menu"),
            id="btn_start_to_menu",
            state=MenuSG.view,
            mode=StartMode.RESET_STACK,
        ),
        getter=today_task_statuses_list_getter,
        state=TodaySG.view,
    ),
)
