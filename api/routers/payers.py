from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import PayerCreate, PayerResponse
from fastapi import APIRouter, Depends, HTTPException
from api.database import get_db
from api import models
from geoalchemy2 import WKTElement
from uuid import UUID
from geoalchemy2.shape import to_shape

router = APIRouter(
    prefix="/payers",
    tags=["payers"]
)

@router.post("/", response_model=PayerResponse)
async def create_payer(payer_data: PayerCreate, db: AsyncSession = Depends(get_db)):
    point_str = f"POINT({payer_data.longitude} {payer_data.latitude})"
    location = WKTElement(point_str, srid=4326)

    new_payer = models.Payer(name=payer_data.name, home_location=location)

    db.add(new_payer)
    await db.commit()
    await db.refresh(new_payer)

    return PayerResponse(
        id=new_payer.id,
        avg_transaction_amount=new_payer.avg_transaction_amount,
        account_created_at=new_payer.account_created_at,
        name=payer_data.name,
        latitude=payer_data.latitude,
        longitude=payer_data.longitude
    )


@router.get("/{payer_id}", response_model=PayerResponse)
async def get_payer_by_id(payer_id: UUID, db: AsyncSession = Depends(get_db)):
    payer = await db.get(models.Payer, payer_id)

    if payer is None:
        raise HTTPException(status_code=404, detail="Payer not found")

    point = to_shape(payer.home_location)

    return PayerResponse(
        id=payer.id,
        name=payer.name,
        account_created_at=payer.account_created_at,
        avg_transaction_amount=payer.avg_transaction_amount,
        longitude=point.x,
        latitude=point.y
    )






