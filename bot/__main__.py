from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import async_sessionmaker
from fluentogram import TranslatorHub
import structlog

from bot.handling.handlers import start_router
from bot.handling.dialogs import first_start_dialog, create_task_dialog
from I18N import i18n_factory
from bot.handling.middlewares import TranslatorRunnerMiddleware, DbSessionMiddleware
from config import Config


async def main(config: Config, session_maker: async_sessionmaker):
    log = structlog.get_logger(__name__)
    log.info("INFO")
    bot = Bot(token=config.token.get_secret_value())
    dp = Dispatcher()

    translator_hub: TranslatorHub = i18n_factory()

    dp.update.middleware(TranslatorRunnerMiddleware(translator_hub))
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=session_maker))

    dp.include_routers(start_router, first_start_dialog, create_task_dialog)
    setup_dialogs(dp)

    await dp.start_polling(bot)
