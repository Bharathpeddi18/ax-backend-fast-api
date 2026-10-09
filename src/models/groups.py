from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Group(Base):
    __tablename__ = "groups"

    group_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    group_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    group_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    group_description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )