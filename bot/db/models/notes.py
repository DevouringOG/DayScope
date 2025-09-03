from sqlalchemy import BigInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.models import Base


class Note(Base):
    """Note model contains text associated with a Day."""

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    day: Mapped[int] = mapped_column(
        ForeignKey("days.id", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"Note(id={self.id!r}, day={self.day!r}, text={self.text!r})"
