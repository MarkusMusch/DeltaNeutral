""" This module contains functions that generate graphs for the funding rate and open interest of ETHBTCUSDT. """
from dash import dcc
import numpy as np
import plotly.graph_objs as go

from backend.crud.crud_funding import read_funding_entries
from backend.crud.crud_open_interest import read_open_interest_entries
from backend.models.models_orm import Symbol
from frontend.src.utils.styling import create_dark_mode_layout


def generate_cumulative_arbitrage_graph() -> dcc.Graph:
    """ 
    This function generates a graph that shows the cumulative return of the ETHBTCUSDT funding rate arbitrage strategy.
    
    Returns:
        dcc.Graph: A Dash graph object that shows the cumulative return of the funding rate arbitrage strategy.
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
    
    cumulative_return_arbitrage = np.cumprod(1 + np.array(funding_rate_difference)) - 1

    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=100*cumulative_return_arbitrage,
                    mode='lines',
                    name='Arbitrage Cumulative Return',
                )
            ],
            'layout': create_dark_mode_layout('ETHBTCUSDT Funding Rate Arbitrage Cummulative Return')
        }
    )


def generate_funding_rates_graph() -> dcc.Graph:
    """ 
    This function generates a graph that shows the funding rates for BTC, ETH and ETHBTC.
    
    Returns:
        dcc.Graph: A Dash graph object that shows the funding rates for BTC, ETH and ETHBTC.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT)
    timestamps_eth, funding_rates_eth = read_funding_entries(Symbol.ETHUSDT)
    timestamps_ethbtc, funding_rates_ethbtc = read_funding_entries(Symbol.ETHBTCUSDT)

    min_entries = min(len(funding_rates_btc), len(funding_rates_eth), len(funding_rates_ethbtc))

    timestamps_btc, funding_rates_btc = timestamps_btc[-min_entries:], funding_rates_btc[-min_entries:]
    timestamps_eth, funding_rates_eth = timestamps_eth[-min_entries:], funding_rates_eth[-min_entries:]
    timestamps_ethbtc, funding_rates_ethbtc = timestamps_ethbtc[-min_entries:], funding_rates_ethbtc[-min_entries:]

    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=funding_rates_btc,
                    mode='lines',
                    name='BTCUSDT Funding Rate'
                ),
                go.Scatter(
                    x=timestamps_eth,
                    y=funding_rates_eth,
                    mode='lines',
                    name='ETHUSDT Funding Rate'
                ),
                go.Scatter(
                    x=timestamps_ethbtc,
                    y=funding_rates_ethbtc,
                    mode='lines',
                    name='ETHBTCUSDT Funding Rate'
                )
            ],
            'layout': create_dark_mode_layout(f'Funding Rate Over Time for ETH, BTC and ETHBTC')
        }
    )


def generate_open_interest_graph() -> dcc.Graph:
    """
    This function generates a graph that shows the open interest for ETHBTCUSDT.

    Returns:
        dcc.Graph: A Dash graph object that shows the open interest for ETHBTCUSDT.
    """
    timestamps_oi_ethbtc, open_interest_ethbtc = read_open_interest_entries(Symbol.ETHBTCUSDT)

    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_oi_ethbtc,
                    y=open_interest_ethbtc,
                    mode='lines',
                    name='Open Interest ETHBTCUSDT'
                )
            ],
            'layout': create_dark_mode_layout('Open Interest ETHBTCUSDT')
        }
    )


def generate_cumulative_funding_rates_graph() -> dcc.Graph:
    """
    This function generates a graph that shows the cumulative return of the funding earned.
    
    Returns:
        dcc.Graph: A Dash graph object that shows the cumulative return of the funding earned.
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
    cumulative_return_btc = np.cumprod(1 + np.array(funding_rates_btc)) - 1
    cumulative_return_eth = np.cumprod(1 + np.array(funding_rates_eth)) - 1
    cumulative_return_ethbtc = np.cumprod(1 + np.array(funding_rates_ethbtc)) - 1
    cumulative_return_arbitrage = np.cumprod(1 + np.array(funding_rate_difference)) - 1
    
    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=cumulative_return_btc * 100,
                    mode='lines',
                    name='BTCUSDT Cumulative Return'
                ),
                go.Scatter(
                    x=timestamps_eth,
                    y=cumulative_return_eth * 100,
                    mode='lines',
                    name='ETHUSDT Cumulative Return'
                ),
                go.Scatter(
                    x=timestamps_ethbtc,
                    y=cumulative_return_ethbtc * 100,
                    mode='lines',
                    name='ETHBTCUSDT Cumulative Return'
                ),
                go.Scatter(
                    x=timestamps_btc,
                    y=cumulative_return_arbitrage * 100,
                    mode='lines',
                    name='Arbitrage Cumulative Return'
                )
            ],
            'layout': create_dark_mode_layout('Cumulative Percentage Return on Funding Earned')
        }
    )