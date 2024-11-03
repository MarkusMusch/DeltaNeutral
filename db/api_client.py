import configparser
import hashlib
import hmac
import requests
import time

from db.models.models_api import (
    FundingHistoryResponse,
    FundingRequest,
    InterestRateResponse,
    OpenInterestRequest,
    OpenInterestResponse
    )

import settings


class ByBitClient:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read(settings.CONFIG_PATH)

        self.api_key = config.get('ByBit Basis Trade', 'api_key')
        self.api_secret = config.get('ByBit Basis Trade', 'api_secret')

        self.base_endpoint = settings.BASE_ENDPOINT_BYBIT
        self.endpoint_funding = settings.ENDPOINT_FUNDING_BYBIT
        self.endpoint_open_interest = settings.ENDPOINT_OPEN_INTEREST_BYBIT

    def _sign_request(self, params: dict) -> str:
        """
        Generate a signature for the given parameters using the API secret.

        Args:
            params (dict): Parameters for the API request.
            api_secret (str): The API secret used to sign the request.

        Returns:
            str: The generated HMAC SHA256 signature.
        """
        param_str = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        return hmac.new(self.api_secret.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_interest_rate(self, currency: str, end_time: int) -> InterestRateResponse:
        url = f"{self.base_endpoint}/v5/spot-margin-trade/interest-rate-history"

        milliseconds_per_day = 24*60*60*1000

        params = {
            "api_key": self.api_key,
            "timestamp":  int(time.time() * 1000),
            "currency": currency,
            "startTime": end_time - 30*milliseconds_per_day,
            "endTime": end_time
        }

        signature = self._sign_request(params)
        params['sign'] = signature

        response = requests.get(url, params=params)
        response_data = response.json()['result']

        if response_data == '{}':
            interestrate_history = InterestRateResponse(list=[])
        else:
            interestrate_history = InterestRateResponse(**response_data)

        return interestrate_history

    def get_funding_history(self, params: FundingRequest) -> FundingHistoryResponse:
        
        url = self.base_endpoint + self.endpoint_funding
       
        response = requests.get(url, params=params.dict())
        response_data = response.json()['result']

        if not response_data['list']:
            funding_history = FundingHistoryResponse(category=params.category,
                                                     list=[])
        else:
            funding_history = FundingHistoryResponse(**response_data)

        return funding_history
    
    def get_open_interest(self, params: OpenInterestRequest) -> OpenInterestResponse:

        url = self.base_endpoint + self.endpoint_open_interest

        response = requests.get(url, params=params.dict())
        response_data = response.json()['result']

        if not response_data['list']:
            open_interest = OpenInterestResponse(category=params.category,
                                                 list=[])
        else:
            open_interest = OpenInterestResponse(**response_data)

        return open_interest