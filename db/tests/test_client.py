import pytest
from unittest.mock import MagicMock, patch
from db.api_client import ByBitClient
from db.models.models_api import FundingRequest, OpenInterestRequest


# Define constants for mocking
MOCK_CONFIG_PATH = "/path/to/config.ini"
MOCK_BASE_ENDPOINT = "https://api.bybit.com"
MOCK_ENDPOINT_FUNDING = "/funding"
MOCK_ENDPOINT_OPEN_INTEREST = "/open_interest"
MOCK_API_KEY = "test_api_key"
MOCK_API_SECRET = "test_api_secret"


@pytest.fixture
def mock_client():
    with patch('db.api_client.configparser.ConfigParser') as mock_cp_class:
        with patch('db.api_client.settings') as mock_settings:

            mock_settings.CONFIG_PATH = MOCK_CONFIG_PATH
            mock_settings.BASE_ENDPOINT_BYBIT = MOCK_BASE_ENDPOINT
            mock_settings.ENDPOINT_FUNDING_BYBIT = MOCK_ENDPOINT_FUNDING
            mock_settings.ENDPOINT_OPEN_INTEREST_BYBIT = MOCK_ENDPOINT_OPEN_INTEREST
 
            mock_cp = MagicMock()
            mock_cp.get.side_effect = lambda section, key: {
                ('ByBit Basis Trade', 'api_key'): MOCK_API_KEY,
                ('ByBit Basis Trade', 'api_secret'): MOCK_API_SECRET
            }[(section, key)]
            mock_cp_class.return_value = mock_cp

            client = ByBitClient()

            yield client


@pytest.fixture
def mock_requests_get():
    with patch('db.api_client.requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_time():
    with patch('db.api_client.time.time') as mock_time_func:
        mock_time_func.return_value = 1700000000.0  # Fixed timestamp
        yield mock_time_func


class TestByBitClient:
    def test_init(self, mock_client):
                
        # Assert that api_key and api_secret are set correctly
        assert mock_client.api_key == MOCK_API_KEY
        assert mock_client.api_secret == MOCK_API_SECRET

        # Assert that base_endpoint is set correctly
        assert mock_client.base_endpoint == MOCK_BASE_ENDPOINT
        assert mock_client.endpoint_funding == MOCK_ENDPOINT_FUNDING
        assert mock_client.endpoint_open_interest == MOCK_ENDPOINT_OPEN_INTEREST

    def test_sign_request(
            self,
            mock_client
        ):
        with patch('db.api_client.hmac.new') as mock_hmac:
            with patch('db.api_client.hashlib.sha256') as mock_hashlib:

                mock_hmac_instance = MagicMock()
                mock_hmac_instance.hexdigest.return_value = MagicMock()
                mock_hmac.return_value = mock_hmac_instance
                
                params = {'b': '2', 'a': '1'}
                signature = mock_client._sign_request(params)

                # Assert that params are sorted and joined correctly
                expected_param_str = "a=1&b=2"
                
                # Assert that hmac.new was called with correct arguments
                mock_hmac.assert_called_once_with(
                    MOCK_API_SECRET.encode('utf-8'),
                    expected_param_str.encode('utf-8'),
                    mock_hashlib
                )

                # Assert that hexdigest was called
                mock_hmac.return_value.hexdigest.assert_called_once()

                # Assert the signature
                assert signature == mock_hmac_instance.hexdigest.return_value

    def test_get_funding_history_empty_list(
        self,
        mock_client,
        mock_requests_get
    ):
        with patch('db.api_client.FundingHistoryResponse') as mock_funding_history_response:
            # Setup mock for requests.get
            mock_response = MagicMock()
            mock_response.json.return_value = {'result': {'category': 'test_category', 'list': []}}
            mock_requests_get.return_value = mock_response

            # Call the method
            result = mock_client.get_funding_history(FundingRequest(category="test_category",
                                                                    symbol="BTCUSD",
                                                                    endTime=1700000000000))

            # Assert that requests.get was called with correct URL and params
            expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_FUNDING

            expected_params = {
                "category": "test_category",
                "symbol": "BTCUSD",
                "endTime": 1700000000000
            }

            mock_requests_get.assert_called_once_with(expected_url, params=expected_params)

            # Assert that FundingHistoryResponse was called with category and empty list
            mock_funding_history_response.assert_called_once_with(category="test_category", list=[])
            assert result == mock_funding_history_response.return_value

    def test_get_funding_history_with_data(
        self,
        mock_client,
        mock_requests_get
    ):
        with patch('db.api_client.FundingHistoryResponse') as mock_funding_history_response:
            # Setup mock for requests.get
            mock_response = MagicMock()
            mock_response.json.return_value = {'result': {'category': 'test_category', 'list': ['data1', 'data2']}}
            mock_requests_get.return_value = mock_response

            # Setup FundingHistoryResponse to return a specific object
            mock_funding_history_response.return_value = "FundingHistoryResponseInstance"

            # Call the method
            result = mock_client.get_funding_history(FundingRequest(category="test_category",
                                                                    symbol="ETHUSD",
                                                                    endTime=1700000000000))

            # Assert that requests.get was called with correct URL and params
            expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_FUNDING
            expected_params = {
                "category": "test_category",
                "symbol": "ETHUSD",
                "endTime": 1700000000000
            }
            
            mock_requests_get.assert_called_once_with(expected_url, params=expected_params)

            # Assert that FundingHistoryResponse was called with the response data
            mock_funding_history_response.assert_called_once_with(**{'category': 'test_category', 'list': ['data1', 'data2']})
            assert result == "FundingHistoryResponseInstance"

    def test_get_open_interest_empty_list(
        self,
        mock_client,
        mock_requests_get
    ):
        with patch('db.api_client.OpenInterestResponse') as mock_open_interest_response:
            # Setup mock for requests.get
            mock_response = MagicMock()
            mock_response.json.return_value = {'result': {'category': 'test_category', 'list': []}}
            mock_requests_get.return_value = mock_response

            # Call the method
            result = mock_client.get_open_interest(OpenInterestRequest(category="test_category",
                                                                       symbol="BTCUSD",
                                                                       intervalTime="1h",
                                                                       endTime=1700000000000))

            # Assert that requests.get was called with correct URL and params
            expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_OPEN_INTEREST

            expected_params = {
                "category": "test_category",
                "symbol": "BTCUSD",
                "intervalTime": "1h",
                "endTime": 1700000000000
            }

            mock_requests_get.assert_called_once_with(expected_url, params=expected_params)

            # Assert that OpenInterestResponse was called with category and empty list
            mock_open_interest_response.assert_called_once_with(category="test_category", list=[])
            assert result == mock_open_interest_response.return_value

    def test_get_open_interest_with_data(
        self,
        mock_client,
        mock_requests_get
    ):
        with patch('db.api_client.OpenInterestResponse') as mock_open_interest_response:
            # Setup mock for requests.get
            mock_response = MagicMock()
            mock_response.json.return_value = {'result': {'category': 'test_category', 'list': ['data1', 'data2']}}
            mock_requests_get.return_value = mock_response

            # Setup OpenInterestResponse to return a specific object
            mock_open_interest_response.return_value = "OpenInterestResponseInstance"

            # Call the method
            result = mock_client.get_open_interest(OpenInterestRequest(category="test_category",
                                                                       symbol="ETHUSD",
                                                                       intervalTime="1h",
                                                                       endTime=1700000000000))

            # Assert that requests.get was called with correct URL and params
            expected_url = MOCK_BASE_ENDPOINT + MOCK_ENDPOINT_OPEN_INTEREST
            expected_params = {
                "category": "test_category",
                "symbol": "ETHUSD",
                "intervalTime": "1h",
                "endTime": 1700000000000
            }

            mock_requests_get.assert_called_once_with(expected_url, params=expected_params)

            # Assert that OpenInterestResponse was called with the response data
            mock_open_interest_response.assert_called_once_with(**{'category': 'test_category', 'list': ['data1', 'data2']})
            assert result == "OpenInterestResponseInstance"

    def test_get_interest_rate_with_empty_result(
        self,
        mock_client,
        mock_requests_get,
        mock_time
    ):
        with patch('db.api_client.InterestRateResponse') as mock_interest_rate_response:
            with patch.object(mock_client, '_sign_request', return_value=MagicMock()) as mock_sign:

                # Setup mock for requests.get
                mock_response = MagicMock()
                mock_response.json.return_value = {'result': '{}'}
                mock_requests_get.return_value = mock_response

                # Call the method
                result = mock_client.get_interest_rate("BTC", 1700000000000)

                # Assert that requests.get was called with correct URL and params
                expected_url = f"{MOCK_BASE_ENDPOINT}/v5/spot-margin-trade/interest-rate-history"
                expected_params = {
                    "api_key": MOCK_API_KEY,
                    "timestamp": 1700000000000,
                    "currency": "BTC",
                    "startTime": 1700000000000 - 30*24*60*60*1000,
                    "endTime": 1700000000000,
                    "sign": mock_sign.return_value
                }
                mock_requests_get.assert_called_once_with(expected_url, params=expected_params)

                # Assert that InterestRateResponse was called with list=[]
                mock_interest_rate_response.assert_called_once_with(list=[])
                assert result == mock_interest_rate_response.return_value

    def test_get_interest_rate_with_data(
        self,
        mock_client,
        mock_requests_get,
        mock_time
    ):
        with patch('db.api_client.InterestRateResponse') as mock_interest_rate_response:
            with patch.object(mock_client, '_sign_request', return_value=MagicMock()) as mock_sign:
                # Setup mock for requests.get
                mock_response = MagicMock()
                mock_response.json.return_value = {'result': {'data': 'some_data'}}
                mock_requests_get.return_value = mock_response

                # Setup InterestRateResponse to return a specific object
                mock_interest_rate_response.return_value = "InterestRateResponseInstance"

                # Call the method
                result = mock_client.get_interest_rate("ETH", 1700000000000)

                # Assert that requests.get was called with correct URL and params
                expected_url = f"{MOCK_BASE_ENDPOINT}/v5/spot-margin-trade/interest-rate-history"
                expected_params = {
                    "api_key": MOCK_API_KEY,
                    "timestamp": 1700000000000,
                    "currency": "ETH",
                    "startTime": 1700000000000 - 30*24*60*60*1000,
                    "endTime": 1700000000000,
                    "sign": mock_sign.return_value
                }
                mock_requests_get.assert_called_once_with(expected_url, params=expected_params)

                # Assert that InterestRateResponse was called with the response data
                mock_interest_rate_response.assert_called_once_with(**{'data': 'some_data'})
                assert result == "InterestRateResponseInstance"