from typing import AsyncGenerator, Generator
from aiogram.types import User
import pytest
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog.test_tools import MockMessageManager, BotClient
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorRunner, TranslatorHub
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
import structlog
import logs

from tests.mocked_aiogram import MockedBot
from bot.handling.middlewares import DbSessionMiddleware, TranslatorRunnerMiddleware
from bot.handling.dialogs import get_dialogs
from bot.handling.handlers import get_routers
from I18N import i18n_factory
from config import parse_config, Config


cfg: Config = parse_config()
logs.startup(cfg.logging)
logger = structlog.get_logger(__name__)

DEFAULT_LOCALE: str = "en"


@pytest.fixture(scope="session")
def config() -> Config:
    logger.info("Parsing config")
    return parse_config()


@pytest.fixture(scope="session")
def bot() -> MockedBot:
    logger.info("Creating MockedBot")
    return MockedBot()


@pytest_asyncio.fixture(scope="session")
async def engine(config: Config) -> AsyncGenerator[AsyncEngine, None]:
    logger.info("Creating async engine")
    engine = create_async_engine(url=str(config.db.dsn))
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def dp(engine: AsyncEngine, message_manager: MockMessageManager) -> Dispatcher:
    logger.info("Creating dispatcher")
    dispatcher = Dispatcher(storage=MemoryStorage())
    logger.info("Setting dispatcher")
    dispatcher.include_routers(*get_routers(), *get_dialogs())
    setup_dialogs(dispatcher, message_manager=message_manager)

    translator_hub: TranslatorHub = i18n_factory()
    dispatcher.update.middleware(TranslatorRunnerMiddleware(translator_hub))

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    dispatcher.update.outer_middleware(DbSessionMiddleware(session_pool=async_session))

    return dispatcher


@pytest.fixture(scope="session")
def user_client(dp: Dispatcher, bot: MockedBot) -> BotClient:
    logger.info("Creating user client")
    client = BotClient(
        dp=dp,
        user_id=123456789,
        chat_id=123456789,
        chat_type="private",
        bot=bot,
    )
    user = User(
        id=1234567,
        is_bot=False,
        first_name="User",
        language_code="en",
    )
    client.user = user
    return client


@pytest.fixture(scope="session")
def i18n() -> TranslatorRunner:
    logger.info("Creating translator runner i18n")
    translator_hub = i18n_factory()
    return translator_hub.get_translator_by_locale(locale=DEFAULT_LOCALE)


@pytest.fixture(scope="session")
def message_manager() -> Generator[MockMessageManager, None, None]:
    logger.info("Creating message manager")
    manager = MockMessageManager()
    yield manager
    logger.info("Resetting message manager history")
    manager.reset_history()


@pytest_asyncio.fixture(scope="session")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncEngine, None]:
    logger.info("Creating session")
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as s:
        yield s
