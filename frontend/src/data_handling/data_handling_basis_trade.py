""" This module contains functions that generate graphs for the funding rates and stable coin interest. """
from dash import dcc
import numpy as np
import plotly.graph_objs as go

from backend.crud.crud_funding import read_funding_entries
from backend.crud.crud_interest import read_interest_entries
from backend.models.models_orm import Coin, Symbol
from frontend.src.utils.styling import create_dark_mode_layout


def generate_cumulative_funding_graph() -> dcc.Graph:
    """ This function generates a graph that shows the cumulative return of the funding rate and stable coin interest.
    
    Returns:
        dcc.Graph: A Dash graph object that shows the cumulative return of the funding rate and stable coin interest.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT, num_values=550)
    # Calculate cumulative percentage return on the funding earned
    cumulative_return_btc = np.cumprod(1 + np.array(funding_rates_btc)) - 1

    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    cumulative_return_dai = np.cumprod(1 + np.array(interest_rates_dai)) - 1

    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=cumulative_return_btc * 100,
                    mode='lines',
                    name='BTCUSDT Funding Cummulative',
                ),
                go.Scatter(
                    x=timestamps_dai,
                    y=cumulative_return_dai * 80,
                    mode='lines',
                    name='DAI Interest Cummulative',
                )
            ],
            'layout': create_dark_mode_layout('Funding Rate and Stable Coin Interest Cummulative')
        }
    )


def generate_funding_rates_graph() -> dcc.Graph:
    """ This function generates a graph that shows the funding rates for BTC and stable coin interest.
    
    Returns:
        dcc.Graph: A Dash graph object that shows the funding rates for BTC and stable coin interest.
    """
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT, num_values=550)
    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    
    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=funding_rates_btc,
                    mode='lines',
                    name='BTCUSDT Funding Rate',
                ),
                go.Scatter(
                    x=timestamps_dai,
                    y=interest_rates_dai,
                    mode='lines',
                    name='DAI Hourly Interest',
                )
            ],
            'layout': create_dark_mode_layout('Funding Rates and Stable Coin Interest')
        }
    )