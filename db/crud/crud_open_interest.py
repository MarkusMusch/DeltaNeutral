from typing import Optional

import numpy as np
from sqlalchemy import desc

from db.config import Session
from db.models.models_orm import OpenInterest, Symbol


def create_open_interest_entries(open_interest_record: OpenInterest):
    with Session() as session:
        try:
            session.merge(open_interest_record)
            session.commit()
        except Exception as e:
            session.rollback()


def read_open_interest_entries(symbol: Symbol, num_values: Optional[int] = None):
    with Session() as session:
        open_interest = (session.query(OpenInterest)
                         .filter_by(symbol=symbol.value)
                         .order_by(desc(OpenInterest.open_interest_timestamp))
                         .limit(num_values)
                         .all())

    timestamps = np.array([rate.open_interest_timestamp for rate in open_interest])[::-1]
    open_interest_values = np.array([float(rate.open_interest) for rate in open_interest])[::-1]
    
    return timestamps, open_interest_values


def read_most_recent_update_open_interest(symbol):
    with Session() as session:
        latest_entry = (session.query(OpenInterest)
                        .filter_by(symbol=symbol.value)
                        .order_by(desc(OpenInterest.open_interest_timestamp))
                        .first())
        
    date_time = latest_entry.open_interest_timestamp

    return date_time