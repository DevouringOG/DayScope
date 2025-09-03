from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start

from bot.custom_widgets import I18nFormat
from bot.dialogs.states import CreateTaskSG, StartSG

"""Dialog shown for new users on first start."""

first_start_dialog = Dialog(
    Window(
        I18nFormat("first-start"),
        Start(
            text=I18nFormat("add-habit"),
            id="add_habit_btn",
            state=CreateTaskSG.enter_title,
        ),
        state=StartSG.start,
    )
)
