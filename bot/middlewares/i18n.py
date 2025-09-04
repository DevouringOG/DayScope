from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    """
    Middleware that injects a translator
    into handler data based on the Telegram user's language.
    """

    def __init__(self, hub: TranslatorHub):
        self.hub = hub
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        data["i18n"] = self.hub.get_translator_by_locale(
            locale=user.language_code
        )

        return await handler(event, data)
