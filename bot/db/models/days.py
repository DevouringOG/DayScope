import datetime

from sqlalchemy import BigInteger, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.models import Base


class Day(Base):
    """Represents a specific calendar date for a user."""

    __tablename__ = "days"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    user: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE")
    )

    __table_args__ = (
        UniqueConstraint("user", "date", name="unique_user_date"),
    )

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"Day(id={self.id!r}, date={self.date!r}, user={self.user!r})"
