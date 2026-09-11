from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.schemas import MerchantCreate, MerchantResponse
from api import models



from uuid import UUID

router = APIRouter(
    prefix="/merchants",
    tags=["merchants"]
)

@router.post("/", response_model=MerchantResponse)
async def create_merchant(merchant_data: MerchantCreate, db: AsyncSession = Depends(get_db)):
    new_merchant = models.Merchant(name=merchant_data.name, category=merchant_data.category)
    db.add(new_merchant)
    await db.commit()
    await db.refresh(new_merchant)
    return new_merchant

@router.get("/{merchant_id}", response_model=MerchantResponse)
async def get_merchant_by_id(merchant_id: UUID, db: AsyncSession = Depends(get_db)):
    merchant = await db.get(models.Merchant, merchant_id)

    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")

    return merchant

