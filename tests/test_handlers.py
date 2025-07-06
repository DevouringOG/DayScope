import asyncio

import pytest
from aiogram_dialog.test_tools import MockMessageManager, BotClient
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
import structlog

from tests.utils import test_user, create_db, assert_single_message_sent
from database.requests import orm_get_user_by_id


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
    await create_db(engine=engine)
    user_client.user = test_user

    await user_client.send(text="/start")

    assert_single_message_sent(message_manager, i18n.first.start())

    response = await orm_get_user_by_id(session, test_user.id)
    assert response is not None, f"User with ID {test_user.id} was not found in the database."
