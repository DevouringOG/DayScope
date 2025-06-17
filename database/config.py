from pydantic import BaseModel, PostgresDsn


class DbConfig(BaseModel):
    dsn: PostgresDsn
