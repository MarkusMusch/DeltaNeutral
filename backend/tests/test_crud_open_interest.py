from datetime import datetime

import numpy as np
import pytest
from sqlalchemy.exc import IntegrityError
from unittest.mock import patch, MagicMock

from backend.models.models_orm import OpenInterest, Symbol
from backend.crud.crud_open_interest import create_open_interest_entries, read_open_interest_entries, read_most_recent_update_open_interest


# Test that OpenInterest entries are added correctly
def test_create_open_interest_entries():
    # Step 1: Mock an OpenInterest object
    open_interest_record = OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000")

    # Step 2: Mock the session and methods using patch
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function to test
        create_open_interest_entries(open_interest_record)

        # Step 3: Verify that merge was called with the correct record
        mock_db_session.merge.assert_called_once_with(open_interest_record)
        mock_db_session.commit.assert_called_once()


# Test that rollback is called when IntegrityError occurs
def test_create_open_interest_entries_integrity_error():
    # Step 1: Mock an OpenInterest object
    open_interest_record = OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000")

    # Step 2: Mock the session and simulate an IntegrityError
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate an IntegrityError on session.commit()
        mock_db_session.commit.side_effect = IntegrityError("mock", "mock", "mock")

        # Call the function to test
        create_open_interest_entries(open_interest_record)

        # Step 3: Verify that rollback was called after IntegrityError
        mock_db_session.rollback.assert_called_once()
        mock_db_session.commit.assert_called_once()


# Test when there are exactly `num_values` records
def test_read_open_interest_entries_exact():
    # Step 1: Mock open interest data
    mock_open_interest = [
        OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000"),
        OpenInterest(symbol=Symbol.BTCUSDT, open_interest="2000.75", open_interest_timestamp="1700000100000")
    ]
    
    # Step 2: Mock the session and query methods
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result
        mock_db_session.query().filter_by().order_by().limit().all.return_value = mock_open_interest

        # Step 3: Call the function
        timestamps, open_interest_values = read_open_interest_entries(Symbol.BTCUSDT, num_values=2)

        # Step 4: Verify the output (timestamps and open interest should be reversed)
        expected_timestamps = np.array([datetime(2023, 11, 14, 22, 13, 20),
                                        datetime(2023, 11, 14, 22, 15)])[::-1]
        expected_open_interest = np.array([1000.50, 2000.75])[::-1]

        np.testing.assert_array_equal(timestamps, expected_timestamps)
        np.testing.assert_array_equal(open_interest_values, expected_open_interest)


# Test when there are fewer than `num_values` records
def test_read_open_interest_entries_fewer_records():
    # Step 1: Mock open interest data with fewer records than `num_values`
    mock_open_interest = [
        OpenInterest(symbol=Symbol.BTCUSDT, open_interest="1000.50", open_interest_timestamp="1700000000000")
    ]
    
    # Step 2: Mock the session and query methods
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result
        mock_db_session.query().filter_by().order_by().limit().all.return_value = mock_open_interest

        # Step 3: Call the function
        timestamps, open_interest_values = read_open_interest_entries(Symbol.BTCUSDT, num_values=5)

        # Step 4: Verify the output (timestamps and open interest should be reversed)
        expected_timestamps = np.array([datetime(2023, 11, 14, 22, 13, 20)])[::-1]
        expected_open_interest = np.array([1000.50])[::-1]

        np.testing.assert_array_equal(timestamps, expected_timestamps)
        np.testing.assert_array_equal(open_interest_values, expected_open_interest)


# Test when there are no records in the database
def test_read_open_interest_entries_no_records():
    # Step 1: No open interest rates to return (empty list)
    mock_open_interest = []

    # Step 2: Mock the session and query methods
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result (empty list)
        mock_db_session.query().filter_by().order_by().limit().all.return_value = mock_open_interest

        # Step 3: Call the function
        timestamps, open_interest_values = read_open_interest_entries(Symbol.BTCUSDT, num_values=5)

        # Step 4: Verify that empty arrays are returned
        np.testing.assert_array_equal(timestamps, np.array([]))
        np.testing.assert_array_equal(open_interest_values, np.array([]))


# Test if the correct query was executed
def test_read_open_interest_entries_query_execution():
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function
        read_open_interest_entries(Symbol.BTCUSDT, num_values=2)

        # Verify that the correct query was executed
        mock_db_session.query.assert_called_once_with(OpenInterest)
        mock_db_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
        mock_db_session.query().filter_by().order_by.assert_called_once()
        mock_db_session.query().filter_by().order_by().limit.assert_called_once_with(2)


# Test when there is a most recent entry
def test_read_most_recent_update_open_interest():
    # Step 1: Mock an OpenInterest object with a timestamp
    mock_latest_entry = OpenInterest(
        symbol=Symbol.BTCUSDT, 
        open_interest="1000.50", 
        open_interest_timestamp="1700000000000"
    )

    # Step 2: Mock the session and query methods
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result returning the latest entry
        mock_db_session.query().filter_by().order_by().first.return_value = mock_latest_entry

        # Step 3: Call the function
        result = read_most_recent_update_open_interest(Symbol.BTCUSDT)

        # Step 4: Verify the returned timestamp
        expected_timestamp = datetime.utcfromtimestamp(1700000000)  # Convert to datetime
        assert result == expected_timestamp


# Test when there are no entries in the database
def test_read_most_recent_update_open_interest_no_entries():
    # Step 1: Simulate no entries by returning None
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result returning None
        mock_db_session.query().filter_by().order_by().first.return_value = None

        # Step 2: Call the function and check it handles None gracefully
        with pytest.raises(AttributeError):
            read_most_recent_update_open_interest(Symbol.BTCUSDT)


# Test if the correct query was executed
def test_read_most_recent_update_open_interest_query_execution():
    with patch("backend.crud.crud_open_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function
        read_most_recent_update_open_interest(Symbol.BTCUSDT)

        # Verify that the correct query was executed
        mock_db_session.query.assert_called_once_with(OpenInterest)
        mock_db_session.query().filter_by.assert_called_once_with(symbol=Symbol.BTCUSDT.value)
        mock_db_session.query().filter_by().order_by.assert_called_once()
        mock_db_session.query().filter_by().order_by().first.assert_called_once()