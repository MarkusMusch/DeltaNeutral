""" This module contains functions that generate graphs for the funding rates and stable coin interest. """
from typing import List, Union

import dash_mantine_components as dmc
import numpy as np

from backend.crud.crud_funding import read_funding_entries
from backend.crud.crud_interest import read_interest_entries
from backend.models.models_orm import Coin, Symbol


def generate_graph_cumulative_funding_leveraged(symbol: Symbol = Symbol.BTCUSDT.value) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ This function generates a graph that shows the cumulative return of the funding rate and stable coin interest.

    Args:
        symbol (Symbol, optional): The symbol for which the cumulative return should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the cumulative return of the funding rate and stable coin interest.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=None)
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

    data = []
    for ts, value, value2, value3 in zip(timestamps_coin, compound_funding_coin, compound_interest_dai, compound_difference):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Compound Funding {symbol}': round(value, 5),
                'Compound Interest DAI': round(value2, 5),
                'Compound Difference': round(value3, 5)
            }
        )

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"{symbol} Funding Rate Cumulative",
                    order=4,
                    mt='xl'
                )
            ]
        ),
        dmc.LineChart(
            h="calc(80vh - 300px)",
            dataKey="date",
            data=data,
            series = [
                {"name": f"Compound Funding {symbol}", "color": "blue.6"},
                {"name": "Compound Interest DAI", "color": "orange.6"},
                {"name": "Compound Difference", "color": "green.6"}
            ],
            referenceLines=[
                {"y": 0, "label": "", "color": "red.6"},
            ],
            curveType="linear",
            tickLine="xy",
            gridAxis="xy",
            withDots=False,
            style={
                "marginTop": "10px",
                "marginBottom": "50px",
                "marginLeft": "50px",
                "marginRight": "50px"
            }
        )
    ]


def generate_graph_funding_rates_leveraged(symbol: Symbol = Symbol.BTCUSDT.value) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ This function generates a graph that shows the funding rates for a Coin and stable coin interest.

    Args:
        symbol (Symbol, optional): The symbol for which the funding rates should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the funding rates for the given coin and
            stable coin interest.
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

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"{symbol} Funding Rate vs. Interest",
                    order=4,
                    mt='xl'
                )
            ]
        ),
        dmc.LineChart(
            h="calc(80vh - 300px)",
            dataKey="date",
            data=data,
            series = [
                {"name": f"Funding {symbol}", "color": "blue.6"},
                {"name": "Interest DAI", "color": "orange.6"}
            ],
            referenceLines=[
                {"y": 0, "label": "", "color": "red.6"},
            ],
            curveType="linear",
            tickLine="xy",
            gridAxis="xy",
            withDots=False,
            style={
                "marginTop": "10px",
                "marginBottom": "50px",
                "marginLeft": "50px",
                "marginRight": "50px"
            }
        )
    ]


def generate_graph_net_income_leveraged(symbol: Symbol = Symbol.BTCUSDT.value) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ This function generates a graph that shows the funding rates for a Coin and stable coin interest.

    Args:
        symbol (Symbol, optional): The symbol for which the funding rates should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the funding rates for the given coin and
            stable coin interest.
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

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"{symbol} Funding Rate vs. Interest",
                    order=4,
                    mt='xl'
                )
            ]
        ),
        dmc.LineChart(
            h="calc(80vh - 300px)",
            dataKey="date",
            data=data,
            series = [
                {"name": "Difference", "color": "green.6"},
                {"name": "Moving Average 30d", "color": "red.6"}
            ],
            referenceLines=[
                {"y": 0, "label": "", "color": "red.6"},
            ],
            curveType="linear",
            tickLine="xy",
            gridAxis="xy",
            withDots=False,
            style={
                "marginTop": "10px",
                "marginBottom": "50px",
                "marginLeft": "50px",
                "marginRight": "50px"
            }
        )
    ]