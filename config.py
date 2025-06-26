from pydantic import BaseModel, SecretStr, PostgresDsn, RedisDsn
from dynaconf import Dynaconf
from typing import Literal


class BotConfig(BaseModel):
    token: SecretStr


class LogsConfig(BaseModel):
    level: Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    time_format: str = "utc"


class DbConfig(BaseModel):
    dsn: PostgresDsn


class RedisConfig(BaseModel):
    dsn: RedisDsn


class Config(BaseModel):
    bot: BotConfig
    logging: LogsConfig
    db: DbConfig
    redis: RedisConfig

    class Config:
        alias_generator = str.upper


def parse_config():
    settings = Dynaconf(
        settings_files=[".secrets.toml", "settings.toml"],
    )
    return Config.model_validate(settings.as_dict())
