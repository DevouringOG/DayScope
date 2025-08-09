from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, ListGroup, Cancel, Start
from bot.handling.custom_widgets import I18NFormat

from bot.handling.states import TodaySG, CreateNote, CurrentNoteSG
from bot.handling.handlers import check_task_button_on_click, to_create_note_onclick
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
        Start(
            text=I18NFormat("note"),
            id="btn_to_create_note",
            state=CreateNote.enter_text,
            data={"day_id", lambda data, widget, manager: data.get("today_id")},
            when=lambda data, widget, manager: not data.get("note_exists"),
        ),
        Start(
            text=I18NFormat("view_note"),
            id="btn_to_view_note",
            state=CurrentNoteSG.view,
            data={"day_id", lambda data, widget, manager: data.get("today_id")},
            when=lambda data, widget, manager: data.get("note_exists"),
        ),
        Cancel(text=I18NFormat("back")),
        getter=today_task_statuses_list_getter,
        state=TodaySG.view,
    ),
)
