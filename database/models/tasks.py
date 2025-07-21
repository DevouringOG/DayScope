from sqlalchemy import BigInteger, Text, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.models import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    user: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"))
