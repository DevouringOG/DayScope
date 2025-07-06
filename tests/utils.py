from sqlalchemy.ext.asyncio import AsyncEngine
from aiogram.types import User
from aiogram_dialog.test_tools import MockMessageManager
from database.models import Base


test_user = User(
    id=1234567,
    is_bot=False,
    first_name="User",
    language_code="en"
)


async def create_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def assert_single_message_sent(message_manager: MockMessageManager, expected_text: str) -> None:
    assert message_manager.sent_messages, "No messages were sent."
    assert len(message_manager.sent_messages) == 1, "Expected exactly one message, but multiple were captured."
    assert message_manager.sent_messages[0].text == expected_text, f"Expected welcome message text '{expected_text}', but got '{message_manager.sent_messages[0].text}'."
