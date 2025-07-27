from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, ListGroup, Cancel, Start, SwitchTo, Back
from bot.handling.custom_widgets import I18NFormat

from bot.handling.states import CreateTaskSG, TasksSG, CurrentTaskSG
from bot.handling.handlers import task_set_title_handler, task_create_handler, task_button_on_click, task_update_value_handler, task_change_title_handler, task_remove
from bot.handling.dialogs.getters import task_list_getter, current_task_getter


TASK_VALUE_RANGE = range(1, 6)


def value_buttons_row(handler):
    return Row(*[
        Button(text=Const(str(i)), id=f"btn_task_value_{i}", on_click=handler)
        for i in TASK_VALUE_RANGE
    ])


create_task_dialog = Dialog(
    Window(
        I18NFormat("enter-title"),
        MessageInput(
            func=task_set_title_handler,
            content_types=ContentType.TEXT,
        ),
        Cancel(text=I18NFormat("back")),
        state=CreateTaskSG.enter_title,
    ),
    Window(
        I18NFormat("enter-value"),
        value_buttons_row(handler=task_create_handler),
        Back(text=I18NFormat("back")),
        state=CreateTaskSG.enter_value,
    )
)

view_tasks_dialog = Dialog(
    Window(
        I18NFormat("tasks-list"),
        ListGroup(
            Button(
                text=Format("{item[title]}"),
                id="btn_task",
                on_click=task_button_on_click,
            ),
            id="tasks_list",
            item_id_getter=lambda x: x["id"],
            items="tasks",
        ),
        Start(
            text=I18NFormat("add-habit"),
            id="btn_start_to_add_habbit",
            state=CreateTaskSG.enter_title,
        ),
        getter=task_list_getter,
        state=TasksSG.view,
    ),
)

view_current_task = Dialog(
    Window(
        I18NFormat("task-view"),
        value_buttons_row(handler=task_update_value_handler),
        Row(
            Cancel(text=I18NFormat("back")),
            SwitchTo(
                text=I18NFormat("remove"),
                state=CurrentTaskSG.confirm_remove,
                id="btn_to_task_remove",
            ),
            SwitchTo(
                text=I18NFormat("task-change-title"),
                state=CurrentTaskSG.change_title,
                id="btn_task_update_title"
            ),
        ),
        getter=current_task_getter,
        state=CurrentTaskSG.view,
    ),
    Window(
        I18NFormat("task-confirm-remove"),
        Row(
            Button(
                text=I18NFormat("remove"),
                on_click=task_remove,
                id="btn_task_remove_confirm",
            ),
            SwitchTo(
                text=I18NFormat("back"),
                state=CurrentTaskSG.view,
                id="btn_back_to_task_view"
            ),
        ),
        state=CurrentTaskSG.confirm_remove,
    ),
    Window(
        I18NFormat("enter-new-title"),
        MessageInput(
            func=task_change_title_handler,
            content_types=ContentType.TEXT,
        ),
        SwitchTo(
            text=I18NFormat("back"),
            state=CurrentTaskSG.view,
            id="btn_back_to_task_view"
        ),
        state=CurrentTaskSG.change_title,
    ),
)
