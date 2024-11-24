""" This module contains functions that generate graphs for the funding rates and stable coin interest. """
from typing import List, Union

import dash_mantine_components as dmc
import numpy as np

from backend.crud.crud_funding import read_funding_entries
from backend.models.models_orm import Symbol


def generate_cumulative_funding_graph(symbol: Symbol = Symbol.BTCUSDT.value) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ This function generates a graph that shows the cumulative return of the funding rate and stable coin interest.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the cumulative return of the funding rate and stable coin interest.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol(symbol), num_values=3*365)
    linear_return_btc = 100 * np.cumsum(np.array(funding_rates_btc))
    cumulative_return_btc = 100 * (np.cumprod(1 + np.array(funding_rates_btc)) - 1)

    data = []
    for ts, value, value2 in zip(timestamps_btc, linear_return_btc, cumulative_return_btc):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Cummulative Funding {symbol}': round(value, 2),
                f'Compounded Funding {symbol}': round(value2, 2)
            }
        )

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"{symbol} Funding Rate Cummulative",
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
                {"name": f"Cummulative Funding {symbol}", "color": "blue.6"},
                {"name": f"Compounded Funding {symbol}", "color": "indigo.6"}
            ],
            curveType="linear",
            tickLine="xy",
            gridAxis="xy",
            withDots=False,
            # withLegend=True,
            style={
                "marginTop": "10px",
                "marginBottom": "50px",
                "marginLeft": "50px",
                "marginRight": "50px"
            }
        )
    ]


def generate_funding_rates_graph(symbol: Symbol = Symbol.BTCUSDT.value) -> List[Union[dmc.Title, dmc.LineChart]]:
    """ This function generates a graph that shows the funding rates for BTC.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the funding rates for BTC.
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
            # withLegend=True,
            style={
                "marginTop": "10px",
                "marginBottom": "50px",
                "marginLeft": "50px",
                "marginRight": "50px"
            }
        )
    ]