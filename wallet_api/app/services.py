from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import Wallet
from fastapi import HTTPException
from decimal import Decimal


async def get_wallet(uuid: str, db: AsyncSession):
    result = await db.execute(select(Wallet).where(Wallet.uuid == uuid))
    wallet = result.scalars().first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


async def update_balance(uuid: str, amount: Decimal, operation: str, db: AsyncSession):
    async with db.begin():
        wallet = await get_wallet(uuid, db)

        if operation == "WITHDRAW" and wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        if operation == "DEPOSIT":
            wallet.balance += amount
        elif operation == "WITHDRAW":
            wallet.balance -= amount

        await db.commit()
        return wallet.balance
