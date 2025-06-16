from typing import Literal

from pydantic import BaseModel


class LogsConfig(BaseModel):
    level: Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    time_format: str = "utc"
