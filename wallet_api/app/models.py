from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"

    uuid = Column(String, primary_key=True, index=True)
    balance = Column(Numeric(10, 2), default=0)
