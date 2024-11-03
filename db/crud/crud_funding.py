from typing import Optional

import numpy as np
from sqlalchemy import desc

from db.config import Session
from db.models.models_orm import FundingRate, Symbol


def create_funding_entries(funding_rate_record: FundingRate):
    with Session() as session:
        try:
            session.merge(funding_rate_record)
            session.commit()
        except Exception as e:
            session.rollback()


def read_funding_entries(symbol: Symbol, num_values: Optional[int] = None):
    with Session() as session:
        funding_rates = (session.query(FundingRate)
                        .filter_by(symbol=symbol.value)
                        .order_by(desc(FundingRate.funding_rate_timestamp))
                        .limit(num_values)
                        .all())

    timestamps = np.array([rate.funding_rate_timestamp for rate in funding_rates])[::-1]
    funding_rates_values = np.array([float(rate.funding_rate) for rate in funding_rates])[::-1]
    
    return timestamps, funding_rates_values


def read_most_recent_update_funding(symbol):
    with Session() as session:
        latest_entry = (session.query(FundingRate)
                            .filter_by(symbol=symbol.value)
                            .order_by(desc(FundingRate.funding_rate_timestamp))
                            .first())
        
    date_time = latest_entry.funding_rate_timestamp

    return date_time