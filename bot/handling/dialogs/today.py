from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, ListGroup, Cancel, Start
from bot.handling.custom_widgets import I18NFormat

from bot.handling.states import TodaySG, CreateNote, CurrentNoteSG
from bot.handling.handlers import check_task_button_on_click
from bot.handling.dialogs.getters import today_task_statuses_list_getter


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
        Start(text=I18NFormat("note"), id="btn_create_note", state=CreateNote.enter_text),
        Cancel(text=I18NFormat("back")),
        getter=today_task_statuses_list_getter,
        state=TodaySG.view,
    ),
)
