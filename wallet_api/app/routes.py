from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import update_balance, get_wallet
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter()

class OperationRequest(BaseModel):
    operation_type: str  # "DEPOSIT" или "WITHDRAW"
    amount: Decimal

@router.get("/api/v1/wallets/{wallet_uuid}")
async def get_wallet_balance(wallet_uuid: str, db: AsyncSession = Depends(get_db)):
    wallet = await get_wallet(wallet_uuid, db)
    return {"wallet_uuid": wallet.uuid, "balance": wallet.balance}

@router.post("/api/v1/wallets/{wallet_uuid}/operation")
async def wallet_operation(wallet_uuid: str, operation: OperationRequest, db: AsyncSession = Depends(get_db)):
    new_balance = await update_balance(wallet_uuid, operation.amount, operation.operation_type, db)
    return {"wallet_uuid": wallet_uuid, "new_balance": new_balance}
