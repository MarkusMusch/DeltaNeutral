""" This module contains CRUD functions for the OpenInterest table. """
from typing import Optional, Tuple

import numpy as np
from sqlalchemy import desc

from backend.config import Session
from backend.models.models_orm import OpenInterest, Symbol


def create_open_interest_entries(open_interest_record: OpenInterest) -> None:
    """Create a new open interest record in the database.

    Args:
        open_interest_record (OpenInterest): The open interest record to be added.
    """
    with Session() as session:
        try:
            session.merge(open_interest_record)
            session.commit()
        except Exception as e:
            print(f"An error occurred while adding open interest record: {e}")
            session.rollback()


def read_open_interest_entries(symbol: Symbol, num_values: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Read open interest records from the database.

    Args:
        symbol (Symbol): The symbol for which the open interest records should be read.
        num_values (int, optional): The number of open interest records to be read. If None, all records are read. Defaults to None.

    Returns:
        tuple: A tuple containing the timestamps and open interest values.
    """
    with Session() as session:
        open_interest = (session.query(OpenInterest)
                         .filter_by(symbol=symbol.value)
                         .order_by(desc(OpenInterest.open_interest_timestamp))
                         .limit(num_values)
                         .all())

    timestamps = np.array([rate.open_interest_timestamp for rate in open_interest])[::-1]
    open_interest_values = np.array([float(rate.open_interest) for rate in open_interest])[::-1]
    
    return timestamps, open_interest_values


def read_most_recent_update_open_interest(symbol: Symbol) -> str:
    """Read the date of the most recent open interest update from the database.

    Args:
        symbol (Symbol): The symbol for which the most recent open interest update should be read.

    Returns:
        str: The timestamp of the most recent open interest update.
    """
    with Session() as session:
        latest_entry = (session.query(OpenInterest)
                        .filter_by(symbol=symbol.value)
                        .order_by(desc(OpenInterest.open_interest_timestamp))
                        .first())
        
    date_time = latest_entry.open_interest_timestamp

    return date_time