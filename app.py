import asyncio

import structlog
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import logs
from bot import bot
from config import parse_config

logger = structlog.get_logger(__name__)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

config = parse_config()

logs.startup(config=config.logging)

logger.info(config.db.dsn)
engine = create_async_engine(url=str(config.db.dsn))
session_maker = async_sessionmaker(engine, expire_on_commit=False)

asyncio.run(bot(config=config, session_maker=session_maker))
