from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start

from bot.handling.custom_widgets import I18NFormat
from bot.handling.dialogs.states import CreateTaskSG, StartSG

first_start_dialog = Dialog(
    Window(
        I18NFormat("first-start"),
        Start(
            text=I18NFormat("add-habit"),
            id="add_habit_btn",
            state=CreateTaskSG.enter_title,
        ),
        state=StartSG.start,
    )
)
