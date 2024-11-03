from pydantic import BaseModel
from typing import List, Tuple
import numpy as np
from datetime import datetime


class FundingRequest(BaseModel):
    category: str
    symbol: str
    endTime: int

class FundingRateItem(BaseModel):
    fundingRate: str
    fundingRateTimestamp: str

class FundingHistoryResponse(BaseModel):
    category: str
    list: List[FundingRateItem]

    @property
    def unpacked_data(self) -> Tuple[np.ndarray, np.ndarray]:
        # Convert timestamps to datetime objects
        timestamps = np.array([datetime.utcfromtimestamp(int(item.fundingRateTimestamp) / 1000) for item in self.list])[::-1]
        funding_rates = np.array([float(item.fundingRate) for item in self.list])[::-1]
        return timestamps, funding_rates

    @property
    def cumulative_return(self) -> np.ndarray:
        # Calculate cumulative return
        _, funding_rates = self.unpacked_data
        return np.cumprod(1 + funding_rates) - 1


class OpenInterestRequest(BaseModel):
    category: str
    symbol: str
    intervalTime: str
    endTime: int

class OpenInterestItem(BaseModel):
    openInterest: str
    timestamp: str

class OpenInterestResponse(BaseModel):
    category: str
    list: List[OpenInterestItem]


class InterestRateItem(BaseModel):
    hourlyBorrowRate: str
    timestamp: int

class InterestRateResponse(BaseModel):
    list: List[InterestRateItem]

    @property
    def unpacked_data(self) -> Tuple[np.ndarray, np.ndarray]:
        datetimes = np.array([datetime.utcfromtimestamp(int(item.timestamp) / 1000) for item in self.list])[::-1]
        interest_rates = np.array([float(item.hourlyBorrowRate) for item in self.list])[::-1]
        return datetimes, interest_rates
    
    @property
    def cumulative_return(self) -> np.ndarray:
        _, interest_rates = self.unpacked_data
        return np.cumprod(1 + interest_rates) - 1