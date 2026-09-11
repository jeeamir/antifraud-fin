from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api import models

from api.schemas import TransactionCreate, TransactionResponse

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction_data: TransactionCreate, db: AsyncSession = Depends(get_db)):

    existing_payer = await db.get(models.Payer, transaction_data.payer_id)
    existing_merchant = await db.get(models.Merchant, transaction_data.merchant_id)

    if existing_payer is None:
        raise HTTPException(status_code=404, detail="Payer not found")

    if existing_merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")


    new_transaction = models.Transaction(payer_id=existing_payer.id, merchant_id=existing_merchant.id, amount=transaction_data.amount, currency=transaction_data.currency)
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)

    return new_transaction
