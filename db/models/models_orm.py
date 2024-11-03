from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Symbol(str, Enum):
    BTCUSDT = 'BTCUSDT'
    ETHUSDT = 'ETHUSDT'
    ETHBTCUSDT = 'ETHBTCUSDT'


class Coin(str, Enum):
    DAI = 'DAI'


class FundingRate(Base):
    __tablename__ = 'funding_rates'

    symbol = Column(SQLEnum(Symbol), primary_key=True, nullable=False)
    funding_rate_timestamp = Column(DateTime, primary_key=True, nullable=False)
    funding_rate = Column(Float, nullable=False)

    def __init__(self, symbol: Symbol, funding_rate: str, funding_rate_timestamp: str):
        self.symbol = symbol
        self.funding_rate = float(funding_rate)
        self.funding_rate_timestamp = datetime.utcfromtimestamp(int(funding_rate_timestamp) / 1000)


class OpenInterest(Base):
    __tablename__ = 'open_interest'

    symbol = Column(SQLEnum(Symbol), primary_key=True, nullable=False)
    open_interest_timestamp = Column(DateTime, primary_key=True, nullable=False)
    open_interest = Column(Float, nullable=False)

    def __init__(self, symbol: Symbol, open_interest: str, open_interest_timestamp: str):
        self.symbol = symbol
        self.open_interest = float(open_interest)
        self.open_interest_timestamp = datetime.utcfromtimestamp(int(open_interest_timestamp) / 1000)


class InterestRate(Base):
    __tablename__ = "interest_rates"

    coin = Column(SQLEnum(Coin), primary_key=True, nullable=False)
    interest_rate_timestamp = Column(DateTime, primary_key=True, nullable=False)
    interest_rate = Column(Float, nullable=False)

    def __init__(self, coin: Coin, interest_rate: str, interest_rate_timestamp: str):
        self.coin = coin 
        self.interest_rate = float(interest_rate)
        self.interest_rate_timestamp = datetime.utcfromtimestamp(int(interest_rate_timestamp) / 1000)