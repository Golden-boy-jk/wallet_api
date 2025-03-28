from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import update_balance, get_wallet
from pydantic import BaseModel, condecimal
from typing import Literal
from uuid import UUID

router = APIRouter()

class OperationRequest(BaseModel):
    operation_type: Literal["DEPOSIT", "WITHDRAW"]  # Строгие значения
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)  # Запрещаем 0 и отрицательные

@router.get("/api/v1/wallets/{wallet_uuid}")
async def get_wallet_balance(wallet_uuid: UUID, db: AsyncSession = Depends(get_db)):
    wallet = await get_wallet(wallet_uuid, db)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"wallet_uuid": wallet.uuid, "balance": wallet.balance}

@router.post("/api/v1/wallets/{wallet_uuid}/operation")
async def wallet_operation(wallet_uuid: UUID, operation: OperationRequest, db: AsyncSession = Depends(get_db)):
    new_balance = await update_balance(wallet_uuid, operation.amount, operation.operation_type, db)
    return {"wallet_uuid": wallet_uuid, "new_balance": new_balance}
