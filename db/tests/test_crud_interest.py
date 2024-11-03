from datetime import datetime

import numpy as np
import pytest
from sqlalchemy.exc import IntegrityError
from unittest.mock import patch, MagicMock

from db.models.models_orm import InterestRate, Coin
from db.crud.crud_interest import create_interest_entries, read_interest_entries, read_most_recent_update_interest


# Test that entries are added in bulk with `add_all`
def test_create_interest_entries():
    # Step 1: Mock a list of InterestRate objects
    interest_rate_record = InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000")

    # Step 2: Mock the session and methods using patch
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function to test
        create_interest_entries(interest_rate_record)

        # Step 3: Verify that add_all was called with the correct records
        mock_db_session.merge.assert_called_once_with(interest_rate_record)
        mock_db_session.commit.assert_called_once()

# Test that rollback is called when IntegrityError occurs
def test_create_interest_entries_integrity_error():
    # Step 1: Mock a list of InterestRate objects
    interest_rate_record = InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000")
    

    # Step 2: Mock the session and simulate an IntegrityError
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate an IntegrityError on session.commit()
        mock_db_session.commit.side_effect = IntegrityError("mock", "mock", "mock")

        # Call the function to test
        create_interest_entries(interest_rate_record)

        # Step 3: Verify that rollback was called after IntegrityError
        mock_db_session.rollback.assert_called_once()
        mock_db_session.commit.assert_called_once()


# Test when there are interest rate records
def test_read_interest_entries():
    # Step 1: Mock interest rate data
    mock_interest_rates = [
        InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000"),
        InterestRate(coin=Coin.DAI, interest_rate="0.04", interest_rate_timestamp="1700000100000")
    ]

    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result
        mock_db_session.query().filter_by().all.return_value = mock_interest_rates

        # Step 3: Call the function
        timestamps, interest_rates_values = read_interest_entries(Coin.DAI)

        # Step 4: Verify the output (timestamps and interest rates should match)
        expected_timestamps = np.array([datetime.utcfromtimestamp(1700000000),
                                        datetime.utcfromtimestamp(1700000100)])
        expected_interest_rates = np.array([0.05, 0.04])

        np.testing.assert_array_equal(timestamps, expected_timestamps)
        np.testing.assert_array_equal(interest_rates_values, expected_interest_rates)


# Test when there are fewer interest rate records
def test_read_interest_entries_fewer_records():
    # Step 1: Mock interest rate data with fewer records
    mock_interest_rates = [
        InterestRate(coin=Coin.DAI, interest_rate="0.05", interest_rate_timestamp="1700000000000")
    ]

    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result
        mock_db_session.query().filter_by().all.return_value = mock_interest_rates

        # Step 3: Call the function
        timestamps, interest_rates_values = read_interest_entries(Coin.DAI)

        # Step 4: Verify the output (only one entry)
        expected_timestamps = np.array([datetime.utcfromtimestamp(1700000000)])
        expected_interest_rates = np.array([0.05])

        np.testing.assert_array_equal(timestamps, expected_timestamps)
        np.testing.assert_array_equal(interest_rates_values, expected_interest_rates)


# Test when there are no records
def test_read_interest_entries_no_records():
    # Step 1: No interest rates to return (empty list)
    mock_interest_rates = []

    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result (empty list)
        mock_db_session.query().filter_by().all.return_value = mock_interest_rates

        # Step 3: Call the function
        timestamps, interest_rates_values = read_interest_entries(Coin.DAI)

        # Step 4: Verify that empty arrays are returned
        np.testing.assert_array_equal(timestamps, np.array([]))
        np.testing.assert_array_equal(interest_rates_values, np.array([]))


# Test if the correct query was executed
def test_read_interest_entries_query_execution():
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function
        read_interest_entries(Coin.DAI)

        # Verify that the correct query was executed
        mock_db_session.query.assert_called_once_with(InterestRate)
        mock_db_session.query().filter_by.assert_called_once_with(coin=Coin.DAI.value)
        mock_db_session.query().filter_by().all.assert_called_once()


# Test when there is a most recent entry
def test_read_most_recent_update_interest():
    # Step 1: Mock an InterestRate object with a timestamp
    mock_latest_entry = InterestRate(
        coin=Coin.DAI,
        interest_rate="0.05",
        interest_rate_timestamp="1700000000000"
    )

    # Step 2: Mock the session and query methods
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result returning the latest entry
        mock_db_session.query().filter_by().order_by().first.return_value = mock_latest_entry

        # Step 3: Call the function
        result = read_most_recent_update_interest(Coin.DAI)

        # Step 4: Verify the returned timestamp
        expected_timestamp = datetime.utcfromtimestamp(1700000000)
        assert result == expected_timestamp


# Test when there are no entries in the database
def test_read_most_recent_update_interest_no_entries():
    # Step 1: Simulate no entries by returning None
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Simulate query result returning None
        mock_db_session.query().filter_by().order_by().first.return_value = None

        # Step 2: Call the function and check it handles None gracefully
        with pytest.raises(AttributeError):
            read_most_recent_update_interest(Coin.DAI)


# Test if the correct query was executed
def test_read_most_recent_update_interest_query_execution():
    with patch("db.crud.crud_interest.Session") as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session

        # Call the function
        read_most_recent_update_interest(Coin.DAI)

        # Verify that the correct query was executed
        mock_db_session.query.assert_called_once_with(InterestRate)
        mock_db_session.query().filter_by.assert_called_once_with(coin=Coin.DAI.value)
        mock_db_session.query().filter_by().order_by.assert_called_once()
        mock_db_session.query().filter_by().order_by().first.assert_called_once()