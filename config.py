from pydantic import BaseModel, PostgresDsn
from dynaconf import Dynaconf

from bot.config import BotConfig
from logs.config import LogsConfig


class DbConfig(BaseModel):
    dsn: PostgresDsn


class Config(BaseModel):
    bot: BotConfig
    db: DbConfig
    logging: LogsConfig

    class Config:
        alias_generator = str.upper


def parse_config():
    settings = Dynaconf(
        settings_files=[".secrets.toml", "settings.toml"],
    )
    return Config.model_validate(settings.as_dict())
