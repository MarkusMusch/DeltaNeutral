""" This module contains the CRUD operations for the InterestRate model. """

from typing import Tuple

import numpy as np
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from backend.config import Session
from backend.models.models_orm import Coin, InterestRate


def create_interest_entries(interest_rate_record: InterestRate) -> None:
    """Create a new interest rate record in the database.

    Args:
        interest_rate_record (InterestRate): The interest rate record to be added.
    """
    with Session() as session:
        try:
            session.merge(interest_rate_record)
            session.commit()
        except Exception as e:
            print(f"An error occurred while adding interest rate record: {e}")
            session.rollback()


def read_interest_entries(coin: Coin) -> Tuple[np.ndarray, np.ndarray]:
    """Read interest rate records from the database.
    
    Args:
        coin (Coin): The coin for which the interest rate records should be read.
        
    Returns:
        tuple: A tuple containing the timestamps and interest rate values.
    """
    try:
        with Session() as session:
            interest_rates = session.query(InterestRate).filter_by(coin=coin.value).all()

        timestamps = np.array([rate.interest_rate_timestamp for rate in interest_rates])
        interest_rates_values = np.array([float(rate.interest_rate) for rate in interest_rates])
        
        return timestamps, interest_rates_values
    except SQLAlchemyError as e:
        print(f"Database error occurred while reading Interest Rate data: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while reading Interest Rate data: {e}")
        raise


def read_most_recent_update_interest(coin: Coin) -> str:
    """Read the date of the most recent interest rate update from the database.

    Args:
        coin (Coin): The coin for which the most recent interest rate update should be read.

    Returns:
        str: The timestamp of the most recent interest rate update.
    """
    try:
        with Session() as session:
            latest_entry = (session.query(InterestRate)
                                .filter_by(coin=coin.value)
                                .order_by(desc(InterestRate.interest_rate_timestamp))
                                .first())
            
        date_time = latest_entry.interest_rate_timestamp

        return date_time
    except SQLAlchemyError as e:
        print(f"Database error occurred while reading the most recent Interest Rate data timestamp: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while reading the most recent Interest Rate data timestamp: {e}")
        raise