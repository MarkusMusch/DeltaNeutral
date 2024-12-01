""" This module contains functions that generate graphs for the funding rates and stable coin interest. """
import numpy as np

from backend.data_access.crud.crud_funding import read_funding_entries
from backend.data_access.crud.crud_interest import read_interest_entries
from backend.models.models_orm import Coin, Symbol


def load_data_cumulative_funding_leveraged(symbol: Symbol = Symbol.BTCUSDT.value):
    """ This function loads the data for the cumulative funding rate graph.

    Args:
        symbol (Symbol, optional): The symbol for which the cumulative return should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=3*365)
    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    first_entry = max(min(timestamps_coin), min(timestamps_dai))

    interest_rates_dai = interest_rates_dai[len(interest_rates_dai) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_dai = timestamps_dai[len(timestamps_dai) % 8::8]

    timestamps_coin = [timestamp for timestamp in timestamps_coin if timestamp >= first_entry][1:]
    timestamps_dai = [timestamp for timestamp in timestamps_dai if timestamp >= first_entry]

    funding_rates_coin = funding_rates_coin[-len(timestamps_coin):]
    interest_rates_dai = interest_rates_dai[-len(timestamps_dai):]
    
    compound_funding_coin = 100*(np.cumprod(1 + np.array(funding_rates_coin)) - 1)
    compound_interest_dai = 100*(np.cumprod(1 + np.array(interest_rates_dai)) - 1)
    compound_difference = 100*(np.cumprod(1 + np.array(funding_rates_coin) - np.array(interest_rates_dai)) - 1)

    title = f"{symbol} Funding Rate Cumulative"

    data = []
    for ts, compound, linear, difference in zip(timestamps_coin, compound_funding_coin, compound_interest_dai, compound_difference):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Compound Funding {symbol}': round(compound, 2),
                'Compound Interest DAI': round(linear, 2),
                'Compound Difference': round(difference, 2)
            }
        )
    
    series = [
        {"name": f"Compound Funding {symbol}", "color": "blue.6"},
        {"name": "Compound Interest DAI", "color": "orange.6"},
        {"name": "Compound Difference", "color": "green.6"}
    ]
    
    return title, data, series


def load_data_funding_rates_leveraged(symbol: Symbol = Symbol.BTCUSDT.value):
    """ This function loads the data for the funding rate graph.

    Args:
        symbol (Symbol, optional): The symbol for which the funding rates should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=None)
    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    first_entry = max(min(timestamps_coin), min(timestamps_dai))

    interest_rates_dai = interest_rates_dai[len(interest_rates_dai) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_dai = timestamps_dai[len(timestamps_dai) % 8::8]

    timestamps_coin = [timestamp for timestamp in timestamps_coin if timestamp >= first_entry][1:]
    timestamps_dai = [timestamp for timestamp in timestamps_dai if timestamp >= first_entry]

    funding_rates_coin = 100*(funding_rates_coin[-len(timestamps_coin):])
    interest_rates_dai = 100*(interest_rates_dai[-len(timestamps_dai):])

    title = f"{symbol} Funding Rate vs. Interest"

    data = []
    for ts, funding, interest in zip(
        timestamps_coin,
        funding_rates_coin,
        interest_rates_dai
    ):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Funding {symbol}': round(funding, 5),
                'Interest DAI': round(interest, 5)
            }
        )
    
    series = [
        {"name": f"Funding {symbol}", "color": "blue.6"},
        {"name": "Interest DAI", "color": "orange.6"}
    ]

    return title, data, series


def load_data_net_income_leveraged(symbol: Symbol = Symbol.BTCUSDT.value):
    """ This function loads the data for the net income graph.

    Args:
        symbol (Symbol, optional): The symbol for which the net income should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        dict: A dictionary containing the timestamps and net income for the given coin.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=None)
    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    first_entry = max(min(timestamps_coin), min(timestamps_dai))

    interest_rates_dai = interest_rates_dai[len(interest_rates_dai) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_dai = timestamps_dai[len(timestamps_dai) % 8::8]

    timestamps_coin = [timestamp for timestamp in timestamps_coin if timestamp >= first_entry][1:]
    timestamps_dai = [timestamp for timestamp in timestamps_dai if timestamp >= first_entry]

    funding_rates_coin = 100*(funding_rates_coin[-len(timestamps_coin):])
    interest_rates_dai = 100*(interest_rates_dai[-len(timestamps_dai):])

    net_income = np.array(funding_rates_coin) - np.array(interest_rates_dai)
    window_size = 30
    moving_average_30d = np.convolve(net_income, np.ones(window_size) / window_size, mode='valid')

    title = f"{symbol} Net Income"

    data = []
    for ts, income, ma30 in zip(
        timestamps_coin,
        net_income,
        moving_average_30d
    ):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                'Difference': round(income, 5),
                'Moving Average 30d': round(ma30, 5)
            }
        )
    
    series = [
        {"name": "Difference", "color": "green.6"},
        {"name": "Moving Average 30d", "color": "red.6"}
    ]

    return title, data, series