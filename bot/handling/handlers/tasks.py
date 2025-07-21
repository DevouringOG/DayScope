from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from fluentogram import TranslatorRunner
import structlog

from bot.handling.states import TasksSG, CurrentTaskSG
from database.requests import orm_add_task


logger = structlog.get_logger(__name__)


async def task_set_title_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    title = message.text
    if title and 1 <= len(title) <= 10:
        dialog_manager.dialog_data["task_title"] = title
        await dialog_manager.next()
        return
    await message.answer(i18n.wrong.habbit.title())


async def task_set_value_handler(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    value = button.widget_id[-1]
    session = dialog_manager.middleware_data["session"]
    task_title = dialog_manager.dialog_data["task_title"]
    await orm_add_task(
        session=session,
        user_telegram_id=callback.from_user.id,
        title=task_title,
        value=value,
    )
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    await callback.message.edit_text(text=i18n.task.added(taskName=task_title))
    await dialog_manager.start(TasksSG.view, show_mode=ShowMode.SEND)


async def task_button_on_click(
        callback: CallbackQuery,
        button: SwitchTo,
        dialog_manager: DialogManager,
):
    await dialog_manager.start(state=CurrentTaskSG.view, data={"current_task_id": dialog_manager.item_id})
