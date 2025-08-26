from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    def __init__(self, hub: TranslatorHub):
        self.hub = hub
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        data["i18n"] = self.hub.get_translator_by_locale(
            locale=user.language_code
        )

        return await handler(event, data)
