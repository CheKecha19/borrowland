# db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BorrowRate(Base):
    __tablename__ = "borrow_rates"
    id = Column(Integer, primary_key=True, index=True)
    exchange = Column(String, index=True)
    asset = Column(String, index=True)
    apr = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class StakingRate(Base):
    __tablename__ = "staking_rates"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)   # биржа или протокол
    asset = Column(String, index=True)
    apr = Column(Float)
    type = Column(String)     # CeFi / DeFi / Native
    timestamp = Column(DateTime, default=datetime.utcnow)
