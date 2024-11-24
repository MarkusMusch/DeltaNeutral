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
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT, num_values=None)
    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    first_entry = max(min(timestamps_btc), min(timestamps_dai))

    interest_rates_dai = interest_rates_dai[len(interest_rates_dai) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_dai = timestamps_dai[len(timestamps_dai) % 8::8]

    timestamps_btc = [timestamp for timestamp in timestamps_btc if timestamp >= first_entry]
    timestamps_dai = [timestamp for timestamp in timestamps_dai if timestamp >= first_entry]

    funding_rates_btc = funding_rates_btc[-len(timestamps_btc):]
    interest_rates_dai = interest_rates_dai[-len(timestamps_dai):]
    
    cumulative_return_btc = np.cumprod(1 + np.array(funding_rates_btc)) - 1
    cumulative_return_dai = np.cumprod(1 + np.array(interest_rates_dai)) - 1
    cumulative_difference = np.cumprod(1 + np.array(funding_rates_btc) - np.array(interest_rates_dai)) - 1
 
    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=100*cumulative_return_btc,
                    mode='lines',
                    name='BTCUSDT Funding Cummulative',
                ),
                go.Scatter(
                    x=timestamps_dai,
                    y=100*cumulative_return_dai,
                    mode='lines',
                    name='DAI Interest Cummulative',
                ),
                go.Scatter(
                    x=timestamps_dai,
                    y=100*cumulative_difference,
                    mode='lines',
                    name='Cummulative Difference of Funding minus Interest',
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
    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT, num_values=None)
    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    first_entry = max(min(timestamps_btc), min(timestamps_dai))

    interest_rates_dai = interest_rates_dai[len(interest_rates_dai) % 8:].reshape(-1, 8).sum(axis=1)
    timestamps_dai = timestamps_dai[len(timestamps_dai) % 8::8]

    timestamps_btc = [timestamp for timestamp in timestamps_btc if timestamp >= first_entry]
    timestamps_dai = [timestamp for timestamp in timestamps_dai if timestamp >= first_entry]

    funding_rates_btc = funding_rates_btc[-len(timestamps_btc):]
    interest_rates_dai = interest_rates_dai[-len(timestamps_dai):]

    net_income = np.array(funding_rates_btc) - np.array(interest_rates_dai) 
    window_size = 30
    moving_average_30d = np.convolve(net_income, np.ones(window_size) / window_size, mode='valid')

    return dcc.Graph(
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=100*funding_rates_btc,
                    mode='lines',
                    name='BTCUSDT Funding Rate',
                ),
                go.Scatter(
                    x=timestamps_dai,
                    y=100*interest_rates_dai,
                    mode='lines',
                    name='DAI Hourly Interest',
                ),
                go.Scatter(
                    x=timestamps_btc,
                    y=100*net_income,
                    mode='lines',
                    name='Cummulative Difference of Funding minus Interest',
                ),
                go.Scatter(
                    x=timestamps_btc[30:],
                    y=100*moving_average_30d,
                    mode='lines',
                    name='Cummulative Difference of Funding minus Interest',
                )
            ],
            'layout': create_dark_mode_layout('Funding Rates and Stable Coin Interest')
        }
    )