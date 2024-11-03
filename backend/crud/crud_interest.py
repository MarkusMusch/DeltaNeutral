import numpy as np
from sqlalchemy import desc

from backend.config import Session
from backend.models.models_orm import Coin, InterestRate


def create_interest_entries(interest_rate_record: InterestRate) -> None:
    with Session() as session:
        try:
            session.merge(interest_rate_record)
            session.commit()
        except Exception as e:
            session.rollback()


def read_interest_entries(coin: Coin):
    with Session() as session:
        interest_rates = session.query(InterestRate).filter_by(coin=coin.value).all()

    timestamps = np.array([rate.interest_rate_timestamp for rate in interest_rates])
    interest_rates_values = np.array([float(rate.interest_rate) for rate in interest_rates])
    
    return timestamps, interest_rates_values


def read_most_recent_update_interest(coin):
    with Session() as session:
        latest_entry = (session.query(InterestRate)
                            .filter_by(coin=coin.value)
                            .order_by(desc(InterestRate.interest_rate_timestamp))
                            .first())
        
    date_time = latest_entry.interest_rate_timestamp

    return date_time