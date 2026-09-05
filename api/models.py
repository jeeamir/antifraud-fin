from typing import Optional
from sqlalchemy import String, Float, Numeric, func, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from decimal import Decimal
import enum
from datetime import datetime
from geoalchemy2 import Geography

class TransactionStatus(enum.Enum):
    PENDING = "pending"
    SCORED = "scored"

class Merchant(Base):
    __tablename__ = "merchant"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50))
    fraud_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    avg_transaction_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10,2), nullable=True)


class Payer(Base):
    __tablename__ = "payer"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    avg_transaction_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    home_location: Mapped[str] = mapped_column(Geography(geometry_type='POINT', srid = 4326))
    account_created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2))
    payer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("payer.id"))
    merchant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("merchant.id"))
    currency: Mapped[str] = mapped_column(String(3))
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    is_fraud: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)


