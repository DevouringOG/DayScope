from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.models import Base


class User(Base):
    """Represents a Telegram user and their basic preferences"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        index=True,
        unique=True,
        nullable=False,
    )
    lang: Mapped[str] = mapped_column(
        Text,
        default="en",
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, telegram_id={self.telegram_id!r}, "
            f"lang={self.lang!r})"
        )
