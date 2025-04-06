from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Wallet
from fastapi import HTTPException
from decimal import Decimal
from uuid import UUID
from app.logger import logger


async def get_wallet(uuid: UUID, db: AsyncSession, for_update: bool = False) -> Wallet:
    logger.info(f"Получение кошелька UUID: {uuid}")

    stmt = select(Wallet).where(Wallet.uuid == uuid)
    if for_update:
        stmt = stmt.with_for_update()

    result = await db.execute(stmt)
    wallet = result.scalars().first()

    if not wallet:
        logger.warning(f"Кошелёк не найден: {uuid}")
        raise HTTPException(status_code=404, detail="Wallet not found")

    return wallet


async def update_balance(
        uuid: UUID, amount: Decimal, operation: str, db: AsyncSession
) -> Decimal:
    async with db.begin():
        logger.info(f"Операция {operation} на сумму {amount} для кошелька {uuid}")
        wallet = await get_wallet(uuid, db, for_update=True)

        if operation == "WITHDRAW":
            if wallet.balance < amount:
                logger.warning(f"Недостаточно средств: {wallet.balance} < {amount}")
                raise HTTPException(status_code=400, detail="Insufficient funds")
            wallet.balance -= amount

        elif operation == "DEPOSIT":
            wallet.balance += amount

        else:
            logger.warning(f"Неверный тип операции: {operation}")
            raise HTTPException(status_code=400, detail="Invalid operation type")

        logger.info(f"Новый баланс кошелька {uuid}: {wallet.balance}")
        return wallet.balance