from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from fluentogram import TranslatorRunner

from bot.handling.states import TasksSG


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
