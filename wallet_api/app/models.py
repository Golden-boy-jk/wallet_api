from sqlalchemy import Column, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"

    # Использование UUID вместо String
    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    balance = Column(Numeric(10, 2), default=0)

    def __repr__(self):
        return f"<Wallet(uuid={self.uuid}, balance={self.balance})>"
