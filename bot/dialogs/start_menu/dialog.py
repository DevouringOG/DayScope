from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, SwitchTo

from bot.custom_widgets import I18nFormat
from bot.dialogs.states import MenuSG, TasksSG, TodaySG

menu_dialog = Dialog(
    Window(
        I18nFormat("menu-text"),
        Start(
            text=I18nFormat("to-today"), id="btn_to_today", state=TodaySG.view
        ),
        Start(
            text=I18nFormat("to-tasks"), id="btn_to_tasks", state=TasksSG.view
        ),
        SwitchTo(
            text=I18nFormat("to-help"), id="btn_to_help", state=MenuSG.help
        ),
        state=MenuSG.view,
    ),
    Window(
        I18nFormat("help-text"),
        SwitchTo(
            text=I18nFormat("to-menu"), id="btn_to_menu", state=MenuSG.view
        ),
        state=MenuSG.help,
    ),
)
