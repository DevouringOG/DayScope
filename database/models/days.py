import datetime

from sqlalchemy import BigInteger, Text, SmallInteger, ForeignKey, Boolean, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.models import Base


class Day(Base):
    __tablename__ = "days"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    user: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("user", "date", name="unique_user_date"),
    )
