import asyncio

import pytest
import structlog
from aiogram_dialog.test_tools import BotClient, MockMessageManager
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.db.requests import orm_get_user_by_id
from tests.utils import assert_single_message_sent

CHAT_ID = 1234567

logger = structlog.get_logger(__name__)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.mark.asyncio
async def test_cmd_start(
    i18n: TranslatorRunner,
    engine: AsyncEngine,
    session: AsyncSession,
    message_manager: MockMessageManager,
    user_client: BotClient,
):
    message_manager.reset_history()

    await user_client.send(text="/start")

    assert_single_message_sent(message_manager, i18n.first.start())

    response = await orm_get_user_by_id(session, user_client.user.id)
    assert (
        response is not None
    ), f"User with ID {user_client.user.id} was not found in the database."


# @pytest.mark.asyncio
# async def test_creating_task(
#     dp: Dispatcher,
#     bot: MockedBot,
#     i18n: TranslatorRunner,
#     engine: AsyncEngine,
#     session: AsyncSession,
#     message_manager: MockMessageManager,
#     user_client: BotClient,
# ):
#     message_manager.reset_history()
#     fsm_context: FSMContext = dp.fsm.get_context(
#         bot=bot, user_id=user_client.user.id, chat_id=CHAT_ID
#     )

#    # 1. Send /start
#     await user_client.send(text="/start")

#     # 2. Get the last message sent (with inline keyboard)
#     last_message = message_manager.one_message()
#     # or .last_message(), depending on your utils

#     # 3. Extract callback data from the inline keyboard
#     # Inline keyboard is usually in last_message.reply_markup.inline_keyboard
#     button = last_message.reply_markup.inline_keyboard[0][0]  # first button

#     # 4. Simulate clicking the inline button
#     await user_client.click(last_message, button)

#     # 5. Assert the expected response
#     assert_single_message_sent(message_manager, i18n.enter.title())


#     # assert_single_message_sent(message_manager, i18n.enter.value())
#     # state = await fsm_context.get_state()
#     # assert state == CreateTaskSG.enter_value
