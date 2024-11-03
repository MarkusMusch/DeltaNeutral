from enum import Enum

from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go

from backend.crud.crud_funding import read_funding_entries
from backend.crud.crud_interest import read_interest_entries
from backend.models.models_orm import Coin, Symbol
from utils.styling import create_dark_mode_layout


class PageInfoBasisTradeLeveraged(str, Enum):
    NAV_LINK = 'Basis Trade Leveraged'
    HREF = '/basis_trade_leveraged'


page_layout_basistrade_leveraged = html.Div(
    children=[
        dcc.Tabs(
            id="page-three-tabs",
            value='tab-1',
            children=[
                dcc.Tab(label='Funding Rate Over Time', value='tab-1'),
                dcc.Tab(label='Explanation', value='tab-2'),
            ],
        ),
        html.Div(id='page-three-tabs-content')
    ],
    style={"maxWidth": "1200px", "margin": "auto", "paddingTop": "50px"}
)


def register_basistrade_leveraged_callbacks(app):
    @app.callback(
        Output('page-three-tabs-content', 'children'),
        Input('page-three-tabs', 'value'),
        prevent_initial_call=True
    )
    def render_content(tab):

        if tab == 'tab-1':
            timestamps_btc, funding_rates_btc = read_funding_entries(Symbol.BTCUSDT, num_values=550)
            # Calculate cumulative percentage return on the funding earned
            cumulative_return_btc = np.cumprod(1 + np.array(funding_rates_btc)) - 1

            timestamps_dai, interest_rates_dai = read_interest_entries(Coin.DAI)
            cumulative_return_dai = np.cumprod(1 + np.array(interest_rates_dai)) - 1
            
            return html.Div(
                children=[
                    html.H3(f'Cummulative Return on BTCUSDT Funding', style={'textAlign': 'center', 'color': 'white'}),
                    dcc.Graph(
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
                    ),
                    html.H3(f'BTCUSDT Funding over Time', style={'textAlign': 'center', 'color': 'white'}),
                    dcc.Graph(
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
                    ),
                    html.H3(f'DAI Cummulative Interest over Time', style={'textAlign': 'center', 'color': 'white'}),
                    dcc.Graph(
                        id='funding-rate-difference-graph',
                        config={"displayModeBar": False},
                        figure={
                            'data': [
                                go.Scatter(
                                    x=timestamps_dai,
                                    y=cumulative_return_dai * 100,
                                    mode='lines',
                                    name='DAI Cummulative Interest',
                                    yaxis='y1'
                                )
                            ],
                            'layout': create_dark_mode_layout('Funding Rate Difference')
                        }
                    ),
                    html.H3(f'DAI Interest over Time', style={'textAlign': 'center', 'color': 'white'}),
                    dcc.Graph(
                        id='funding-rate-difference-graph',
                        config={"displayModeBar": False},
                        figure={
                            'data': [
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
                ],
                style={"backgroundColor": "#111111"}
            )
        elif tab == 'tab-2':
            # Calculate and display summary statistics
            return html.Div(
                children=[
                    html.H3(f'Explanation of the trades rationale', style={'textAlign': 'center', 'color': 'white'}),
                    html.Div([
                        html.P(f'One goes long spot short perps to earn funding rate while being delta neutral.', style={'color': 'white'}),
                        html.P(f'Because the position is delta neutral, high leverage can be applied.', style={'color': 'white'})
                    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '4px', 'backgroundColor': '#222222'})
                ],
                style={"backgroundColor": "#111111"}
            )