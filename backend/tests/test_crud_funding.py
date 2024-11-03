from datetime import datetime

import numpy as np
import pytest
from sqlalchemy.exc import IntegrityError
from unittest.mock import patch, MagicMock

from backend.models.models_orm import FundingRate, Symbol
from backend.crud.crud_funding import create_funding_entries, read_funding_entries, read_most_recent_update_funding


# Test that entries are added in bulk with `add_all`
def test_create_funding_entries():
    # Step 1: Mock a list of FundingRate objects
    funding_rate_record = FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000")

    # Step 2: Mock the session and methods using patch
    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function to test
        create_funding_entries(funding_rate_record)

        # Step 3: Verify that add_all was called with the correct records
        mock_db_session.merge.assert_called_once_with(funding_rate_record)
        mock_db_session.commit.assert_called_once()


# Test that rollback is called when IntegrityError occurs
def test_create_funding_entries_integrity_error():
    # Step 1: Mock a list of FundingRate objects
    funding_rate_record = FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000")
    

    # Step 2: Mock the session and simulate an IntegrityError
    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate an IntegrityError on session.commit()
        mock_db_session.commit.side_effect = IntegrityError("mock", "mock", "mock")

        # Call the function to test
        create_funding_entries(funding_rate_record)

        # Step 3: Verify that rollback was called after IntegrityError
        mock_db_session.rollback.assert_called_once()
        mock_db_session.commit.assert_called_once()


# Test when there are exactly `num_values` records
def test_read_funding_entries_exact():
    # Step 1: Mock funding rate data
    mock_funding_rates = [
        FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000"),
        FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.02", funding_rate_timestamp="1700000100000")
    ]
    
    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result
        mock_db_session.query().filter_by().order_by().limit().all.return_value = mock_funding_rates

        # Step 3: Call the function
        timestamps, funding_rates_values = read_funding_entries(Symbol.BTCUSDT, num_values=2)

        # Step 4: Verify the output (timestamps and funding rates should be reversed)
        expected_timestamps = np.array([datetime(2023, 11, 14, 22, 13, 20),
                                        datetime(2023, 11, 14, 22, 15)])[::-1]
        expected_funding_rates = np.array([0.01, 0.02])[::-1]

        np.testing.assert_array_equal(timestamps, expected_timestamps)
        np.testing.assert_array_equal(funding_rates_values, expected_funding_rates)


# Test when there are fewer than `num_values` records
def test_read_funding_entries_fewer_records():
    # Step 1: Mock funding rate data with fewer records than `num_values`
    mock_funding_rates = [
        FundingRate(symbol=Symbol.BTCUSDT, funding_rate="0.01", funding_rate_timestamp="1700000000000")
    ]
    
    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result
        mock_db_session.query().filter_by().order_by().limit().all.return_value = mock_funding_rates

        # Step 3: Call the function
        timestamps, funding_rates_values = read_funding_entries(Symbol.BTCUSDT, num_values=5)

        # Step 4: Verify the output (timestamps and funding rates should be reversed)
        expected_timestamps = np.array([datetime(2023, 11, 14, 22, 13, 20)])[::-1]
        expected_funding_rates = np.array([0.01])[::-1]

        np.testing.assert_array_equal(timestamps, expected_timestamps)
        np.testing.assert_array_equal(funding_rates_values, expected_funding_rates)


# Test when there are no records in the database
def test_read_funding_entries_no_records():
    # Step 1: No funding rates to return (empty list)
    mock_funding_rates = []

    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result (empty list)
        mock_db_session.query().filter_by().order_by().limit().all.return_value = mock_funding_rates

        # Step 3: Call the function
        timestamps, funding_rates_values = read_funding_entries(Symbol.BTCUSDT, num_values=5)

        # Step 4: Verify that empty arrays are returned
        np.testing.assert_array_equal(timestamps, np.array([]))
        np.testing.assert_array_equal(funding_rates_values, np.array([]))


# Test if the correct query was executed
def test_read_funding_entries_query_execution():

    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function
        read_funding_entries(Symbol.BTCUSDT, num_values=2)

        # Verify that the correct query was executed
        mock_db_session.query.assert_called_once_with(FundingRate)
        mock_db_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
        mock_db_session.query().filter_by().order_by.assert_called_once()
        mock_db_session.query().filter_by().order_by().limit.assert_called_once_with(2)


# Test when there is a most recent entry
def test_read_most_recent_update_funding():
    # Step 1: Mock a FundingRate object with a timestamp
    mock_latest_entry = FundingRate(
        symbol=Symbol.BTCUSDT, 
        funding_rate="0.01", 
        funding_rate_timestamp="1700000000000"
    )

    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result returning the latest entry
        mock_db_session.query().filter_by().order_by().first.return_value = mock_latest_entry

        # Step 3: Call the function
        result = read_most_recent_update_funding(Symbol.BTCUSDT)

        # Step 4: Verify the returned timestamp
        assert result == datetime(2023, 11, 14, 22, 13, 20)


# Test when there are no entries in the database
def test_read_most_recent_update_funding_no_entries():
    # Step 1: Simulate no entries by returning None
    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result returning None
        mock_db_session.query().filter_by().order_by().first.return_value = None

        # Step 2: Call the function and check it handles None gracefully
        with pytest.raises(AttributeError):
            read_most_recent_update_funding(Symbol.BTCUSDT)


# Test if the correct query was executed
def test_read_most_recent_update_funding_query_execution():

    with patch("db.crud.crud_funding.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function
        read_most_recent_update_funding(Symbol.BTCUSDT)

        # Verify that the correct query was executed
        mock_db_session.query.assert_called_once_with(FundingRate)
        mock_db_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
        mock_db_session.query().filter_by().order_by.assert_called_once()
        mock_db_session.query().filter_by().order_by().first.assert_called_once()