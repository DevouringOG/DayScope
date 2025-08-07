from sqlalchemy import BigInteger, Text, SmallInteger, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database.models import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    day: Mapped[int] = mapped_column(ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text)
