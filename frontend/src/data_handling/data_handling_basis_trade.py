""" This module contains functions that generate graphs for the funding rates and stable coin interest. """
from typing import List, Union

import dash_mantine_components as dmc
import numpy as np

from backend.crud.crud_funding import read_funding_entries
from backend.models.models_orm import Symbol


def generate_graph_cumulative_funding(symbol: Symbol = Symbol.BTCUSDT.value) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ This function generates a graph that shows the cumulative return of the funding rate.

    Args:
        symbol (Symbol, optional): The symbol for which the cumulative return should be calculated.
            Defaults to Symbol.BTCUSDT.value.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the cumulative return of the funding rate and stable coin interest.
    """
    timestamps_coin, funding_rates_coin = read_funding_entries(Symbol(symbol), num_values=3*365)
    linear_return_coin = 100 * np.cumsum(np.array(funding_rates_coin))
    cumulative_return_btc = 100 * (np.cumprod(1 + np.array(funding_rates_coin)) - 1)

    data = []
    for ts, compound, linear in zip(timestamps_coin, cumulative_return_btc, linear_return_coin):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Compound Funding {symbol}': round(compound, 2),
                f'Cummulative Funding {symbol}': round(linear, 2)
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
                {"name": f"Compound Funding {symbol}", "color": "indigo.6"},
                {"name": f"Cummulative Funding {symbol}", "color": "blue.6"}
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


def generate_graph_funding_rates(symbol: Symbol = Symbol.BTCUSDT.value) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ This function generates a graph that shows the funding rates for the given coin.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the funding rates for the given coin.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol(symbol), num_values=3*365)
    
    data = []
    for ts, value in zip(timestamps_btc, funding_rates_btc):
        data.append({'date': ts.strftime('%b %y'), f'Funding {symbol}': round(100*value, 5)})

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"{symbol} Funding Rate",
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