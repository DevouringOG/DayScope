import asyncio

import structlog
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import logs
from bot import bot
from config import parse_config

logger = structlog.get_logger(__name__)
logger.info("Starting DayScope application")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logger.info("Event loop policy set to WindowsSelectorEventLoopPolicy")

config = parse_config()
logger.info("Configuration parsed successfully", config=config)

logs.startup(config=config.logging)
logger.info("Logging system initialized")

engine = create_async_engine(url=str(config.db.dsn))
logger.info("Database engine created")

session_maker = async_sessionmaker(engine, expire_on_commit=False)
logger.info("Session maker created", session_maker=session_maker)

logger.info("Starting bot")
asyncio.run(bot(config=config, session_maker=session_maker))
