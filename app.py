import asyncio

from bot import bot
from config import parse_config
import logs


config = parse_config()
logs.startup(config=config.logging)

asyncio.run(bot(config=config.bot))
