import uuid
from uuid import UUID
from fastapi import HTTPException, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
from api import models
from api.schemas import TransactionCreate, TransactionAccepted, TransactionResponse

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/", response_model=TransactionAccepted)
async def create_transaction(transaction_data: TransactionCreate, request: Request, db: AsyncSession = Depends(get_db)):

    existing_payer = await db.get(models.Payer, transaction_data.payer_id)
    existing_merchant = await db.get(models.Merchant, transaction_data.merchant_id)

    if existing_payer is None:
        raise HTTPException(status_code=404, detail="Payer not found")

    if existing_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")

    generate_id = uuid.uuid4()

    new_transaction = {
        "id": generate_id,
        "payer_id": transaction_data.payer_id,
        "merchant_id": transaction_data.merchant_id,
        "amount": transaction_data.amount,
        "currency": transaction_data.currency,
    }

    await request.app.state.kafka_producer.send_and_wait(
        "transactions_raw",
        new_transaction
    )

    response = {
        "id": generate_id,
        "status": "ACCEPTED"
    }

    return response


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_by_id(transaction_id: UUID, db: AsyncSession = Depends(get_db)):
    transaction = await db.get(models.Transaction, transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction is not found")

    return transaction



