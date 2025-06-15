from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from bot.handling.custom_widgets import I18NFormat
from fluentogram import TranslatorRunner


from bot.handling.states import CreateTaskSG, TasksSG


async def title_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    title = message.text
    if title and 1 <= len(title) <= 10:
        await dialog_manager.next()
        return
    await message.answer(i18n.wrong.habbit.title())


async def value_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    value = int(message.text)
    if value and 1 <= value <= 5:
        await dialog_manager.switch_to(state=TasksSG.view)
        return
    await message.answer(i18n.wrong.habbit.value())


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