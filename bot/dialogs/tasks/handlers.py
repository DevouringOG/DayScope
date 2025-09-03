import structlog
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode, SubManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo

from bot.db.requests import (
    orm_add_task,
    orm_task_change_title,
    orm_task_remove,
    orm_task_update_value,
)
from bot.dialogs.states import CurrentTaskSG, TasksSG
from bot.utils import get_i18n

logger = structlog.get_logger(__name__)


TITLE_LENGTH_RANGE = range(1, 11)


def is_valid_title(title: str) -> bool:
    """Return True when title length is within allowed range."""
    return bool(title) and len(title) in TITLE_LENGTH_RANGE


async def task_set_title_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """Validate and save the task title from user input.

    Moves the dialog to the next step when validation succeeds.
    """
    title = message.text
    if is_valid_title(title):
        dialog_manager.dialog_data["task_title"] = title
        await dialog_manager.next()
        return

    i18n = get_i18n(dialog_manager)
    await message.answer(i18n.wrong.habit.title())


async def task_create_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Validate value and create the task."""
    value = button.widget_id[-1]
    session = dialog_manager.middleware_data["session"]
    task_title = dialog_manager.dialog_data.get("task_title", "")
    await orm_add_task(
        session=session,
        user_telegram_id=callback.from_user.id,
        title=task_title,
        value=value,
    )

    i18n = get_i18n(dialog_manager)
    await callback.message.edit_text(
        text=i18n.task.added(task_title=task_title)
    )
    await dialog_manager.start(TasksSG.view, show_mode=ShowMode.SEND)


async def task_button_on_click_handler(
    callback: CallbackQuery, button: SwitchTo, dialog_manager: SubManager
) -> None:
    """Navigate to the selected task's detailed view."""
    await dialog_manager.start(
        state=CurrentTaskSG.view,
        data={"current_task_id": int(dialog_manager.item_id)},
    )


async def task_update_value_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    """Update an existing task's value based on the clicked button."""
    session = dialog_manager.middleware_data["session"]
    task_id = dialog_manager.start_data["current_task_id"]
    new_value = int(button.widget_id[-1])
    await orm_task_update_value(session, task_id, new_value)

    i18n = get_i18n(dialog_manager)
    task_title = dialog_manager.dialog_data.get("task_title", "")
    await callback.message.edit_text(
        i18n.task.view(title=task_title, value=new_value)
    )


async def task_change_title_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """Change the title of the current task using user input."""
    old_title = dialog_manager.dialog_data.get("task_title", "")
    new_title = message.text
    if not is_valid_title(title=new_title):
        i18n = get_i18n(dialog_manager)
        await message.answer(i18n.wrong.habit.title())
        return

    session = dialog_manager.middleware_data["session"]
    task_id = dialog_manager.start_data.get("current_task_id")

    await orm_task_change_title(session, task_id, new_title)
    dialog_manager.dialog_data["task_title"] = new_title

    i18n = get_i18n(dialog_manager)
    await message.answer(
        i18n.title.update.success(old_title=old_title, new_title=new_title)
    )
    await dialog_manager.switch_to(state=CurrentTaskSG.view)


async def task_remove_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    """Handle task deletion."""
    session = dialog_manager.middleware_data["session"]
    task_id = dialog_manager.start_data.get("current_task_id")

    await orm_task_remove(session, task_id)

    i18n = get_i18n(dialog_manager)
    task_title = dialog_manager.dialog_data.get("task_title", "")
    await callback.message.edit_text(i18n.task.remove(task_title=task_title))
    await dialog_manager.start(
        state=TasksSG.view, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND
    )
