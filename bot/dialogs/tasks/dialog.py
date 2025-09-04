from aiogram.enums import ContentType
from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    ListGroup,
    Row,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from bot.custom_widgets import I18nFormat
from bot.dialogs.states import (
    CreateTaskSG,
    CurrentTaskSG,
    MenuSG,
    TasksSG,
)
from bot.dialogs.tasks.getters import (
    current_task_getter,
    task_list_getter,
)
from bot.dialogs.tasks.handlers import (
    task_button_handler,
    task_change_title_handler,
    task_change_value_handler,
    task_create_handler,
    task_remove_handler,
    task_set_title_handler,
)

TASK_VALUE_RANGE = range(1, 6)


def value_buttons_row(handler):
    return Row(
        *[
            Button(
                text=Const(str(i)), id=f"btn_task_value_{i}", on_click=handler
            )
            for i in TASK_VALUE_RANGE
        ]
    )


create_task_dialog = Dialog(
    Window(
        I18nFormat("enter-title"),
        MessageInput(
            func=task_set_title_handler, content_types=ContentType.TEXT
        ),
        Cancel(text=I18nFormat("back")),
        state=CreateTaskSG.enter_title,
    ),
    Window(
        I18nFormat("enter-value"),
        value_buttons_row(handler=task_create_handler),
        Back(text=I18nFormat("back")),
        state=CreateTaskSG.enter_value,
    ),
)

tasks_view_dialog = Dialog(
    Window(
        I18nFormat("tasks-list"),
        ListGroup(
            Button(
                text=Format("{item[title]}"),
                id="btn_task",
                on_click=task_button_handler,
            ),
            id="tasks_list",
            item_id_getter=lambda x: x["id"],
            items="tasks",
        ),
        Row(
            Start(
                text=I18nFormat("to-menu"),
                id="btn_start_to_menu",
                state=MenuSG.view,
                mode=StartMode.RESET_STACK,
            ),
            Start(
                text=I18nFormat("add-habit"),
                id="btn_start_to_add_habit",
                state=CreateTaskSG.enter_title,
            ),
        ),
        getter=task_list_getter,
        state=TasksSG.view,
    )
)

view_current_task = Dialog(
    Window(
        I18nFormat("task-view"),
        value_buttons_row(handler=task_change_value_handler),
        Row(
            Cancel(text=I18nFormat("back")),
            SwitchTo(
                text=I18nFormat("remove"),
                state=CurrentTaskSG.confirm_remove,
                id="btn_to_task_remove",
            ),
            SwitchTo(
                text=I18nFormat("task-change-title"),
                state=CurrentTaskSG.change_title,
                id="btn_task_change_title",
            ),
        ),
        getter=current_task_getter,
        state=CurrentTaskSG.view,
    ),
    Window(
        I18nFormat("task-confirm-remove"),
        Row(
            Button(
                text=I18nFormat("remove"),
                on_click=task_remove_handler,
                id="btn_task_remove_confirm",
            ),
            SwitchTo(
                text=I18nFormat("back"),
                state=CurrentTaskSG.view,
                id="btn_back_to_task_view",
            ),
        ),
        state=CurrentTaskSG.confirm_remove,
    ),
    Window(
        I18nFormat("enter-new-title"),
        MessageInput(
            func=task_change_title_handler, content_types=ContentType.TEXT
        ),
        SwitchTo(
            text=I18nFormat("back"),
            state=CurrentTaskSG.view,
            id="btn_back_to_task_view",
        ),
        state=CurrentTaskSG.change_title,
    ),
)
