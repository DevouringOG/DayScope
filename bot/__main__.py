import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub

from bot.handling.handlers import start_router
from bot.handling.dialogs import first_start_dialog, create_task_dialog
from I18N import i18n_factory
from bot.handling.middlewares import TranslatorRunnerMiddleware


logging.basicConfig(
    level=logging.DEBUG,
    format="[{asctime}] #{levelname:8} {filename}:{lineno} - {name} - {message}",
    style="{",
)

logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token="8012464002:AAFFN0TGnDYtrPBm1NWDs7MIvLTEkwPD8dA")
    dp = Dispatcher()

    dp.include_routers(start_router, first_start_dialog, create_task_dialog)
    setup_dialogs(dp)

    translator_hub: TranslatorHub = i18n_factory()
    dp.update.middleware(TranslatorRunnerMiddleware(translator_hub))

    await dp.start_polling(bot)
