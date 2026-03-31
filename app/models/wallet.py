from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0.00"), nullable=False
    )
