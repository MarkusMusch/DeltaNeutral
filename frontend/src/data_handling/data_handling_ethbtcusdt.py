""" This module contains functions that generate graphs for the funding rate and open interest of ETHBTCUSDT. """
from typing import List, Union

from dash import dcc
import dash_mantine_components as dmc
import numpy as np
import plotly.graph_objs as go

from backend.crud.crud_funding import read_funding_entries
from backend.crud.crud_open_interest import read_open_interest_entries
from backend.models.models_orm import Symbol


def generate_graph_cumulative_arbitrage() -> List[Union[dmc.Title, dmc.LineChart]]:
    """ 
    This function generates a graph that shows the cumulative return of the ETHBTCUSDT funding rate arbitrage strategy.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the cumulative return of the funding
            rate arbitrage strategy.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT)
    timestamps_eth, funding_rates_eth = read_funding_entries(Symbol.ETHUSDT)
    timestamps_ethbtc, funding_rates_ethbtc = read_funding_entries(Symbol.ETHBTCUSDT)

    min_entries = min(len(funding_rates_btc), len(funding_rates_eth), len(funding_rates_ethbtc))

    timestamps_btc, funding_rates_btc = timestamps_btc[-min_entries:], funding_rates_btc[-min_entries:]
    timestamps_eth, funding_rates_eth = timestamps_eth[-min_entries:], funding_rates_eth[-min_entries:]
    timestamps_ethbtc, funding_rates_ethbtc = timestamps_ethbtc[-min_entries:], funding_rates_ethbtc[-min_entries:]
 
    # Calculate the difference: BTCUSDT + ETHBTCUSDT - ETHUSDT
    funding_rate_difference= (
        funding_rates_btc +
        funding_rates_ethbtc -
        funding_rates_eth
    )
    
    compound_return_arbitrage = 100*(np.cumprod(1 + np.array(funding_rate_difference)) - 1)

    data = []
    for ts, compound in zip(timestamps_btc, compound_return_arbitrage):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Compound Funding Difference': round(compound, 2),
            }
        )

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"Compound Funding Difference",
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
                {"name": "Compound Funding Difference", "color": "indigo.6"},
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


def generate_graph_funding_rates() -> List[Union[dmc.Title, dmc.LineChart]]:
    """ 
    This function generates a graph that shows the funding rates for BTC, ETH and ETHBTC.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the funding rates for BTC, ETH and ETHBTC.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT)
    timestamps_eth, funding_rates_eth = read_funding_entries(Symbol.ETHUSDT)
    timestamps_ethbtc, funding_rates_ethbtc = read_funding_entries(Symbol.ETHBTCUSDT)

    min_entries = min(len(funding_rates_btc), len(funding_rates_eth), len(funding_rates_ethbtc))

    timestamps_btc, funding_rates_btc = timestamps_btc[-min_entries:], funding_rates_btc[-min_entries:]
    timestamps_eth, funding_rates_eth = timestamps_eth[-min_entries:], funding_rates_eth[-min_entries:]
    timestamps_ethbtc, funding_rates_ethbtc = timestamps_ethbtc[-min_entries:], funding_rates_ethbtc[-min_entries:]

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


    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"Funding Rates BTC, ETH, ETHBTC",
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
                {"name": "BTC Funding", "color": "blue.6"},
                {"name": "ETH Funding", "color": "orange.6"},
                {"name": "ETHBTC Funding", "color": "green.6"}
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


def generate_graph_open_interest() -> List[Union[dmc.Title, dmc.LineChart]]:
    """
    This function generates a graph that shows the open interest for ETHBTCUSDT.

    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the open interest for ETHBTCUSDT.
    """
    timestamps_oi_ethbtc, open_interest_ethbtc = read_open_interest_entries(Symbol.ETHBTCUSDT)


    data = []
    for ts, oi in zip(timestamps_oi_ethbtc, open_interest_ethbtc):
        data.append(
            {
                'date': ts.strftime('%b %y'),
                f'Open Interest': round(oi, 2),
            }
        )

    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"Open Interest ETHBTCUSDT",
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
                {"name": "Open Interest", "color": "indigo.6"}
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



def generate_graph_cumulative_funding_rates() -> List[Union[dmc.Title, dmc.LineChart]]:
    """
    This function generates a graph that shows the cumulative return of the funding earned.
    
    Returns:
        List[Union[dmc.Title, dmc.LineChart]]: A Dash graph object that shows the cumulative return of the funding earned.
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


    return [
        dmc.Center(
            children=[
                dmc.Title(
                    f"Compound Funding Rates BTC, ETH, ETHBTC, Arbitrage",
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
                {"name": "BTC Funding Compound", "color": "blue.6"},
                {"name": "ETH Funding Compound", "color": "orange.6"},
                {"name": "ETHBTC Funding Compound", "color": "green.6"},
                {"name": "Arbitrage Funding", "color": "red.6"}
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

