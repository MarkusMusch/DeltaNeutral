""" This module contains functions that generate graphs for the funding rate and open interest of ETHBTCUSDT. """
import numpy as np

from backend.crud.crud_funding import read_funding_entries
from backend.crud.crud_open_interest import read_open_interest_entries
from backend.models.models_orm import Symbol


def load_data_cumulative_arbitrage():
    """ This function loads the data for the cumulative arbitrage funding rate graph.

    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT)
    timestamps_eth, funding_rates_eth = read_funding_entries(Symbol.ETHUSDT)
    timestamps_ethbtc, funding_rates_ethbtc = read_funding_entries(Symbol.ETHBTCUSDT)

    min_entries = min(len(funding_rates_btc), len(funding_rates_eth), len(funding_rates_ethbtc))

    timestamps_btc, funding_rates_btc = timestamps_btc[-min_entries:], funding_rates_btc[-min_entries:]
    timestamps_eth, funding_rates_eth = timestamps_eth[-min_entries:], funding_rates_eth[-min_entries:]
    timestamps_ethbtc, funding_rates_ethbtc = timestamps_ethbtc[-min_entries:], funding_rates_ethbtc[-min_entries:]

    # Calculate the difference: BTCUSDT + ETHBTCUSDT - ETHUSDT
    funding_rate_difference = (
        funding_rates_btc +
        funding_rates_ethbtc -
        funding_rates_eth
    )

    compound_return_arbitrage = 100*(np.cumprod(1 + np.array(funding_rate_difference)) - 1)

    title = f"Compound Funding Difference ETHBTCUSDT"

    data = []
    for ts, compound in zip(timestamps_btc, compound_return_arbitrage):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Compound Funding Difference': round(compound, 2),
            }
        )
    
    series = [
        {"name": f"Compound Funding Difference", "color": "indigo.6"}
    ]

    return title, data, series


def load_data_funding_rates_ethbtcusdt():
    """ This function loads the data for the funding rates graph.

    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT)
    timestamps_eth, funding_rates_eth = read_funding_entries(Symbol.ETHUSDT)
    timestamps_ethbtc, funding_rates_ethbtc = read_funding_entries(Symbol.ETHBTCUSDT)

    min_entries = min(len(funding_rates_btc), len(funding_rates_eth), len(funding_rates_ethbtc))

    timestamps_btc, funding_rates_btc = timestamps_btc[-min_entries:], funding_rates_btc[-min_entries:]
    timestamps_eth, funding_rates_eth = timestamps_eth[-min_entries:], funding_rates_eth[-min_entries:]
    timestamps_ethbtc, funding_rates_ethbtc = timestamps_ethbtc[-min_entries:], funding_rates_ethbtc[-min_entries:]

    title = f"Funding Rates BTC, ETH, ETHBTC"

    data = []
    for ts, funding_btc, funding_eth, funding_ethbtc in zip(
        timestamps_btc,
        funding_rates_btc,
        funding_rates_eth,
        funding_rates_ethbtc
    ):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                'BTC Funding': round(funding_btc, 5),
                'ETH Funding': round(funding_eth, 5),
                'ETHBTC Funding': round(funding_ethbtc, 5)
            }
        )

    series = [
        {"name": "BTC Funding", "color": "blue.6"},
        {"name": "ETH Funding", "color": "orange.6"},
        {"name": "ETHBTC Funding", "color": "green.6"}
    ]

    return title, data, series


def load_data_open_interest():
    """ This function loads the data for the open interest graph.

    Returns:
        dict: A dictionary containing the timestamps and open interest for the given coin.
    """
    timestamps_oi_ethbtc, open_interest_ethbtc = read_open_interest_entries(Symbol.ETHBTCUSDT)

    title = f"Open Interest ETHBTCUSDT"

    data = []
    for ts, oi in zip(timestamps_oi_ethbtc, open_interest_ethbtc):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Open Interest': round(oi, 2),
            }
        )

    series = [
        {"name": f"Open Interest", "color": "indigo.6"}
    ]

    return title, data, series


def load_data_cumulative_funding_ethbtcusdt():
    """ This function loads the data for the cumulative funding rates graph.

    Returns:
        dict: A dictionary containing the timestamps and funding rates for the given coin.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT)
    timestamps_eth, funding_rates_eth = read_funding_entries(Symbol.ETHUSDT)
    timestamps_ethbtc, funding_rates_ethbtc = read_funding_entries(Symbol.ETHBTCUSDT)

    min_entries = min(len(funding_rates_btc), len(funding_rates_eth), len(funding_rates_ethbtc))

    timestamps_btc, funding_rates_btc = timestamps_btc[-min_entries:], funding_rates_btc[-min_entries:]
    timestamps_eth, funding_rates_eth = timestamps_eth[-min_entries:], funding_rates_eth[-min_entries:]
    timestamps_ethbtc, funding_rates_ethbtc = timestamps_ethbtc[-min_entries:], funding_rates_ethbtc[-min_entries:]

    # Calculate the difference: BTCUSDT + ETHBTCUSDT - ETHUSDT
    funding_rate_difference = (
        funding_rates_btc +
        funding_rates_ethbtc -
        funding_rates_eth
    )

    # Calculate cumulative percentage return on the funding earned
    compound_return_btc = np.cumprod(1 + np.array(funding_rates_btc)) - 1
    compound_return_eth = np.cumprod(1 + np.array(funding_rates_eth)) - 1
    compound_return_ethbtc = np.cumprod(1 + np.array(funding_rates_ethbtc)) - 1
    compound_return_arbitrage = np.cumprod(1 + np.array(funding_rate_difference)) - 1

    title = f"Compound Funding Rates BTC, ETH, ETHBTC, Arbitrage"

    data = []
    for ts, funding_btc, funding_eth, funding_ethbtc, arb in zip(
        timestamps_btc,
        compound_return_btc,
        compound_return_eth,
        compound_return_ethbtc,
        compound_return_arbitrage
    ):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                'BTC Funding Compound': round(funding_btc, 5),
                'ETH Funding Compound': round(funding_eth, 5),
                'ETHBTC Funding Compound': round(funding_ethbtc, 5),
                'Arbitrage Funding': round(arb, 5)
            }
        )

    series = [
        {"name": "BTC Funding Compound", "color": "blue.6"},
        {"name": "ETH Funding Compound", "color": "orange.6"},
        {"name": "ETHBTC Funding Compound", "color": "green.6"},
        {"name": "Arbitrage Funding", "color": "red.6"}
    ]

    return title, data, series