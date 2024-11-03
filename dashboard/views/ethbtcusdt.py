from enum import Enum

from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

from db.crud.crud_funding import read_funding_entries
from db.crud.crud_open_interest import read_open_interest_entries
from db.models.models_orm import Symbol
from dashboard.utils.styling import create_dark_mode_layout


class PageInfoETHBTCUSDT(str, Enum):
    NAV_LINK = 'ETHBTCUSDT'
    HREF = '/ethbtcusdt'

page_layout_ethbtcusdt = html.Div(
    children=[
        dcc.Tabs(
            id="page-one-tabs",
            value='tab-1',
            children=[
                dcc.Tab(label='Funding Rate Over Time', value='tab-1'),
                dcc.Tab(label='Explanation', value='tab-2'),
            ],
        ),
        html.Div(id='page-one-tabs-content')
    ],
    style={"maxWidth": "1200px", "margin": "auto", "paddingTop": "50px"}
)


def register_ethbtcusdt_callbacks(app):
    @app.callback(
        Output('page-one-tabs-content', 'children'),
        Input('page-one-tabs', 'value')
    )
    def render_content(tab):
        timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT)
        timestamps_eth, funding_rates_eth = read_funding_entries(Symbol.ETHUSDT)
        timestamps_ethbtc, funding_rates_ethbtc = read_funding_entries(Symbol.ETHBTCUSDT)

        min_entries = min(len(funding_rates_btc), len(funding_rates_eth), len(funding_rates_ethbtc))

        timestamps_btc, funding_rates_btc = timestamps_btc[-min_entries:], funding_rates_btc[-min_entries:]
        timestamps_eth, funding_rates_eth = timestamps_eth[-min_entries:], funding_rates_eth[-min_entries:]
        timestamps_ethbtc, funding_rates_ethbtc = timestamps_ethbtc[-min_entries:], funding_rates_ethbtc[-min_entries:]

        timestamps_oi_ethbtc, open_interest_ethbtc = read_open_interest_entries(Symbol.ETHBTCUSDT)

        if tab == 'tab-1':
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

            return html.Div(
                children=[

                    dcc.Graph(
                        id='funding-rate-difference-graph',
                        config={"displayModeBar": False},
                        figure={
                            'data': [
                                go.Scatter(
                                    x=timestamps_btc,
                                    y=25*100*cumulative_return_arbitrage,
                                    mode='lines',
                                    name='Arbitrage Cumulative Return',
                                )
                            ],
                            'layout': create_dark_mode_layout('Funding Rate Arbitrage Cummulative Return')
                        }
                    ),
                    dcc.Graph(
                        id='funding-rate-graph',
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
                    ),
                    dcc.Graph(
                        id='open-interest-graph',
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
                    ),
                    dcc.Graph(
                        id='cumulative-return-graph',
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
                ],
                style={"backgroundColor": "#111111"}
            )
        elif tab == 'tab-2':
            # Calculate and display summary statistics
            return html.Div(
                children=[
                    html.H3(f'Explanation of the trades rationale', style={'textAlign': 'center', 'color': 'white'}),
                    html.Div([
                        html.P(f'One takes advantage of the mispricing of ETHBTCUSDT vs ETHUSDT and BTCUSDT.', style={'color': 'white'}),
                        html.P(f'Because the position is delta neutral, high leverage can be applied.', style={'color': 'white'})
                    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '4px', 'backgroundColor': '#222222'})
                ],
                style={"backgroundColor": "#111111"}
            )