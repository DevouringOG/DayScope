from pydantic import BaseModel, SecretStr, PostgresDsn, RedisDsn, ConfigDict
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
    model_config = ConfigDict(alias_generator=str.upper)

    bot: BotConfig
    logging: LogsConfig
    db: DbConfig
    redis: RedisConfig


def parse_config():
    settings = Dynaconf(
        settings_files=[".secrets.toml", "settings.toml"],
    )
    return Config.model_validate(settings.as_dict())
