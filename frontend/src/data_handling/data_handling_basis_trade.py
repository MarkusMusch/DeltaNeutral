from dash import dcc
import numpy as np
import plotly.graph_objs as go

from backend.crud.crud_funding import read_funding_entries
from backend.crud.crud_interest import read_interest_entries
from backend.models.models_orm import Coin, Symbol
from frontend.src.utils.styling import create_dark_mode_layout


def generate_cumulative_funding_graph() -> dcc.Graph:

    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT, num_values=550)
    # Calculate cumulative percentage return on the funding earned
    cumulative_return_btc = np.cumprod(1 + np.array(funding_rates_btc)) - 1

    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    cumulative_return_dai = np.cumprod(1 + np.array(interest_rates_dai)) - 1

    return dcc.Graph(
        id='funding-rate-difference-graph',
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=cumulative_return_btc * 100,
                    mode='lines',
                    name='BTCUSDT Funding',
                    yaxis='y1'
                ),
                go.Scatter(
                    x=timestamps_dai,
                    y=cumulative_return_dai * 80,
                    mode='lines',
                    name='DAI Interest',
                    yaxis='y1'
                )
            ],
            'layout': create_dark_mode_layout('Funding Rate Cummulative')
        }
    )


def generate_funding_rates_graph() -> dcc.Graph:

    timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT, num_values=550)
    # Calculate cumulative percentage return on the funding earned

    timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
    
    return dcc.Graph(
        id='funding-rate-difference-graph',
        config={"displayModeBar": False},
        figure={
            'data': [
                go.Scatter(
                    x=timestamps_btc,
                    y=funding_rates_btc,
                    mode='lines',
                    name='BTCUSDT',
                    yaxis='y1'
                ),
                go.Scatter(
                    x=timestamps_dai,
                    y=interest_rates_dai,
                    mode='lines',
                    name='DAI Hourly Interest',
                    yaxis='y1'
                )
            ],
            'layout': create_dark_mode_layout('Funding Rate Difference')
        }
    )