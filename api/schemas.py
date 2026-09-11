from datetime import datetime

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from decimal import Decimal
from api.models import TransactionStatus

class MerchantCreate(BaseModel):
    name: str
    category: str

class MerchantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category: str
    fraud_rate: Optional[float] = None
    avg_transaction_amount: Optional[Decimal] = None

class PayerCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

class PayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    latitude: float
    longitude: float
    avg_transaction_amount: Optional[Decimal] = None
    account_created_at: datetime

class TransactionCreate(BaseModel):
    payer_id: UUID
    merchant_id: UUID
    amount: Decimal
    currency: str


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    payer_id: UUID
    merchant_id: UUID
    amount: Decimal
    currency: str
    timestamp: datetime
    status: TransactionStatus
    is_fraud: Optional[bool] = None








