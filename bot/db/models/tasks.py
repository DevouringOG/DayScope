from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    SmallInteger,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.models import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    value: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    user: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
    )


class TaskStatus(Base):
    __tablename__ = "task_status"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    task: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tasks.id", ondelete="CASCADE"),
    )
    day: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("days.id", ondelete="CASCADE"),
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    __table_args__ = (UniqueConstraint("task", "day", name="task_day_unique"),)
