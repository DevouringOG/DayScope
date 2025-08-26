from typing import Literal

from dynaconf import Dynaconf
from pydantic import BaseModel, ConfigDict, PostgresDsn, RedisDsn, SecretStr


class BotConfig(BaseModel):
    token: SecretStr


class LogsConfig(BaseModel):
    level: Literal[
        "CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG"
    ] = "INFO"
    time_format: str = "utc"


class DbConfig(BaseModel):
    dsn: PostgresDsn


class RedisConfig(BaseModel):
    dsn: RedisDsn


class Config(BaseModel):
    model_config = ConfigDict(alias_generator=str.upper)

    bot: BotConfig
    logging: LogsConfig
    db: DbConfig
    redis: RedisConfig


def parse_config():
    settings = Dynaconf(settings_files=[".secrets.toml", "settings.toml"])
    return Config.model_validate(settings.as_dict())
