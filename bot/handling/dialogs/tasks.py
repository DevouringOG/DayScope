from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from bot.handling.custom_widgets import I18NFormat

from bot.handling.states import CreateTaskSG
from bot.handling.handlers import title_handler, value_handler


create_task_dialog = Dialog(
    Window(
        I18NFormat("enter-title"),
        MessageInput(
            func=title_handler,
            content_types=ContentType.TEXT,
        ),
        state=CreateTaskSG.enter_title,
    ),
    Window(
        I18NFormat("enter-value"),
        MessageInput(
            func=value_handler,
            content_types=ContentType.TEXT,
        ),
        state=CreateTaskSG.enter_value,
    )
)
