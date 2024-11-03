from enum import Enum

from dash import dcc, html
from dash.dependencies import Input, Output


class PageInfoShort(str, Enum):
    NAV_LINK = 'Short'
    HREF = '/short'


page_layout_short = html.Div(
    children=[
        dcc.Tabs(
            id="page-five-tabs",
            value='tab-1',
            children=[
                dcc.Tab(label='Charts of Coin Pairs', value='tab-1'),
                dcc.Tab(label='Explanation', value='tab-2'),
            ],
        ),
        html.Div(id='page-five-tabs-content')
    ],
    style={"maxWidth": "1200px", "margin": "auto", "paddingTop": "50px"}
)


def register_short_callbacks(app):
    @app.callback(
        Output('page-five-tabs-content', 'children'),
        Input('page-five-tabs', 'value')
    )
    def render_content(tab):

        if tab == 'tab-1':
            # Calculate and display summary statistics
            return html.Div(
                children=[
                    html.H3(f'Graphical depiction of the trade over time.', style={'textAlign': 'center', 'color': 'white'}),
                    html.Div([
                        html.P(f'This page will show plots of the Short Trade', style={'color': 'white'})
                    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '4px', 'backgroundColor': '#222222'})
                ],
                style={"backgroundColor": "#111111"}
            )
        elif tab == 'tab-2':
            # Calculate and display summary statistics
            return html.Div(
                children=[
                    html.H3(f'Explanation of the trades rationale', style={'textAlign': 'center', 'color': 'white'}),
                    html.Div([
                        html.P(f'One goes long some dominant coin and short a weaker coin.', style={'color': 'white'}),
                        html.P(f'The long short setup decreases volatility substantially over going naked short.', style={'color': 'white'})
                    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '4px', 'backgroundColor': '#222222'})
                ],
                style={"backgroundColor": "#111111"}
            )