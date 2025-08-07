from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from bot.handling.custom_widgets import I18NFormat

from bot.handling.states import MenuSG, TasksSG, TodaySG


menu_dialog = Dialog(
    Window(
        I18NFormat("menu-text"),
        Start(text=I18NFormat("to-today"), id="btn_to_today", state=TodaySG.view),
        Start(text=I18NFormat("to-tasks"), id="btn_to_tasks", state=TasksSG.view),
        SwitchTo(text=I18NFormat("to-help"), id="btn_to_help", state=MenuSG.help),
        state=MenuSG.view,
    ),
    Window(
        I18NFormat("help-text"),
        SwitchTo(text=I18NFormat("to-menu"), id="btn_to_menu", state=MenuSG.view),
        state=MenuSG.help,
    ),
)
