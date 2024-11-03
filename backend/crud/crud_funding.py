""" This module contains CRUD functions for the funding rate data. """

from typing import Optional, Tuple

import numpy as np
from sqlalchemy import desc

from backend.config import Session
from backend.models.models_orm import FundingRate, Symbol


def create_funding_entries(funding_rate_record: FundingRate) -> None:
    """Create a new funding rate record in the database.
    
    Args:
        funding_rate_record (FundingRate): The funding rate record to be added.
    """
    with Session() as session:
        try:
            session.merge(funding_rate_record)
            session.commit()
        except Exception as e:
            print(f"An error occurred while adding funding rate record: {e}")
            session.rollback()


def read_funding_entries(symbol: Symbol, num_values: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Read funding rate records from the database.

    Args:
        symbol (Symbol): The symbol for which the funding rate records should be read.
        num_values (int, optional): The number of funding rate records to be read. If None, all records are read. Defaults to None.

    Returns:
        tuple: A tuple containing the timestamps and funding rate values.
    """
    with Session() as session:
        funding_rates = (session.query(FundingRate)
                        .filter_by(symbol=symbol.value)
                        .order_by(desc(FundingRate.funding_rate_timestamp))
                        .limit(num_values)
                        .all())

    timestamps = np.array([rate.funding_rate_timestamp for rate in funding_rates])[::-1]
    funding_rates_values = np.array([float(rate.funding_rate) for rate in funding_rates])[::-1]
    
    return timestamps, funding_rates_values


def read_most_recent_update_funding(symbol: Symbol) -> str:
    """Read the date of the most recent funding rate update from the database.

    Args:
        symbol (Symbol): The symbol for which the most recent funding rate update should be read.

    Returns:
        str: The timestamp of the most recent funding rate update.
    """
    with Session() as session:
        latest_entry = (session.query(FundingRate)
                            .filter_by(symbol=symbol.value)
                            .order_by(desc(FundingRate.funding_rate_timestamp))
                            .first())
        
    date_time = latest_entry.funding_rate_timestamp

    return date_time