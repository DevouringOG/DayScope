from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, ListGroup, Cancel, SwitchTo
from bot.handling.custom_widgets import I18NFormat

from bot.handling.states import CreateTaskSG, TasksSG, CurrentTaskSG
from bot.handling.handlers import task_set_title_handler, task_set_value_handler, task_button_on_click, task_update_value_handler, task_change_title_handler
from bot.handling.dialogs.getters import get_tasks_getter, current_task_getter


create_task_dialog = Dialog(
    Window(
        I18NFormat("enter-title"),
        MessageInput(
            func=task_set_title_handler,
            content_types=ContentType.TEXT,
        ),
        state=CreateTaskSG.enter_title,
    ),
    Window(
        I18NFormat("enter-value"),
        Row(
            Button(
                text=Const("1"),
                id="value_btn_1",
                on_click=task_set_value_handler,
            ),
            Button(
                text=Const("2"),
                id="value_btn_2",
                on_click=task_set_value_handler,
            ),
            Button(
                text=Const("3"),
                id="value_btn_3",
                on_click=task_set_value_handler,
            ),
            Button(
                text=Const("4"),
                id="value_btn_4",
                on_click=task_set_value_handler,
            ),
            Button(
                text=Const("5"),
                id="value_btn_5",
                on_click=task_set_value_handler,
            ),
        ),
        state=CreateTaskSG.enter_value,
    )
)

view_tasks_dialog = Dialog(
    Window(
        I18NFormat("tasks-list"),
        ListGroup(
            Button(
                text=Format("{item[title]}"),
                on_click=task_button_on_click,
                id="task_btn",
            ),
            id="tasks_list",
            item_id_getter=lambda x: str(x["id"]),
            items="tasks",
        ),
        getter=get_tasks_getter,
        state=TasksSG.view,
    ),
)

view_current_task = Dialog(
    Window(
        I18NFormat("task-view"),
        Row(
            Button(
                text=Const("1"),
                id="value_btn_1",
                on_click=task_update_value_handler,
            ),
            Button(
                text=Const("2"),
                id="value_btn_2",
                on_click=task_update_value_handler,
            ),
            Button(
                text=Const("3"),
                id="value_btn_3",
                on_click=task_update_value_handler,
            ),
            Button(
                text=Const("4"),
                id="value_btn_4",
                on_click=task_update_value_handler,
            ),
            Button(
                text=Const("5"),
                id="value_btn_5",
                on_click=task_update_value_handler,
            ),
        ),
        SwitchTo(
            text=I18NFormat("task-change-title"),
            state=CurrentTaskSG.change_title,
            id="btn_task_update_title"
        ),
        Cancel(text=I18NFormat("back")),
        getter=current_task_getter,
        state=CurrentTaskSG.view,
    ),
    Window(
        I18NFormat("enter-new-title"),
        MessageInput(
            func=task_change_title_handler,
            content_types=ContentType.TEXT,
        ),
        state=CurrentTaskSG.change_title,
    ),
)
