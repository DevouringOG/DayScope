from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub
import structlog

from bot.handling.handlers import start_router
from bot.handling.dialogs import first_start_dialog, create_task_dialog
from I18N import i18n_factory
from bot.handling.middlewares import TranslatorRunnerMiddleware
from config import Config


async def main(config: Config):
    log = structlog.get_logger(__name__)
    log.info("INFO")
    bot = Bot(token=config.token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(start_router, first_start_dialog, create_task_dialog)
    setup_dialogs(dp)

    translator_hub: TranslatorHub = i18n_factory()
    dp.update.middleware(TranslatorRunnerMiddleware(translator_hub))

    await dp.start_polling(bot)
