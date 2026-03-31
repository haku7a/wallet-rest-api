import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.wallet import Wallet
from app.schemas.wallet import WalletResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_wallet(db: AsyncSession = Depends(get_db)):
    wallet = Wallet(uuid=uuid4())
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    logger.info("Wallet created: %s", wallet.uuid)
    return {"uuid": str(wallet.uuid), "balance": float(wallet.balance)}


@router.get("/", response_model=list[WalletResponse])
async def list_wallets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Wallet))
    wallets = result.scalars().all()
    logger.info("Wallets listed: found %d", len(wallets))
    return [{"uuid": str(w.uuid), "balance": float(w.balance)} for w in wallets]
