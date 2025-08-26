from aiogram_dialog.test_tools import MockMessageManager

# async def create_db(engine: AsyncEngine):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


def assert_single_message_sent(
    message_manager: MockMessageManager, expected_text: str
) -> None:
    assert message_manager.sent_messages, "No messages were sent."
    assert (
        len(message_manager.sent_messages) == 1
    ), "Expected exactly one message, but multiple were captured."
    assert message_manager.sent_messages[0].text == expected_text, (
        f"Expected message text '{expected_text}', "
        f"but got '{message_manager.sent_messages[0].text}'."
    )
