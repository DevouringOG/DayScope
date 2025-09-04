import structlog
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.dialogs import get_dialogs
from bot.dialogs.start_menu.handlers import start_router
from bot.i18n_factory import get_translator_hub
from bot.middlewares import (
    DbSessionMiddleware,
    TranslatorRunnerMiddleware,
)
from config import Config


async def main(config: Config, session_maker: async_sessionmaker) -> None:
    logger = structlog.get_logger(__name__)

    bot = Bot(token=config.bot.token.get_secret_value())
    logger.info("bot.created")

    storage = RedisStorage.from_url(
        url=str(config.redis.dsn),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    logger.info("storage.created")
    dp = Dispatcher(storage=storage)

    translator_hub: TranslatorHub = get_translator_hub()
    logger.info("translator.hub_initialized")

    dp.update.middleware(TranslatorRunnerMiddleware(translator_hub))
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=session_maker))
    logger.info("middlewares.attached")

    dialogs = get_dialogs()
    dp.include_routers(start_router, *dialogs)
    logger.info("routers.included")

    setup_dialogs(dp)
    logger.info("dialogs.setup_completed")

    await dp.start_polling(bot)
