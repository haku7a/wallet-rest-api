import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.wallet import Wallet
from app.schemas.wallet import BalanceResponse, WalletResponse

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


@router.get("/{wallet_uuid}", response_model=BalanceResponse)
async def get_wallet_balance(wallet_uuid, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Wallet).where(Wallet.uuid == wallet_uuid))
    wallet = result.scalar_one_or_none()
    if not wallet:
        logger.warning("Wallet not found: %s", wallet_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found"
        )
    logger.info("Balance requested for wallet: %s", wallet_uuid)
    return {"balance": float(wallet.balance)}
