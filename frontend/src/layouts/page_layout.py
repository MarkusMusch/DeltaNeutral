""" This module contains the layout of the page. """
from enum import Enum
from dash import dcc, html
import dash_mantine_components as dmc

from frontend.src.components.tabs.basis_trade import generate_tab_basis_trade
from frontend.src.components.tabs.ethbtcusdt import generate_tab_ethbtcusdt
from frontend.src.components.tabs.short import generate_tab_short


class PageIds(Enum):
    TAB_ONE = 'page-one-tabs'

page_layout = html.Div(
    children=[
        dmc.Tabs(
            id=PageIds.TAB_ONE.value,
            value='tab-1',
            children=[
                dmc.TabsList(
                    children=[
                        dcc.Store(
                            id='tab-1-store',
                            data={'active_carousel': 0}
                        ),
                        dmc.TabsTab(
                            value='tab-1',
                            children="Arbitrage ETHBTCUSDT",
                        ),
                        dcc.Store(
                            id='tab-2-store',
                            data={'active_carousel': 0}
                        ),
                        dmc.TabsTab(
                            value='tab-2',
                            children="Basis Trade",
                        ),
                        dmc.TabsTab(
                            value='tab-3',
                            children="Short",
                        )
                    ]
                ),
                dmc.TabsPanel(
                    id='tab-1',
                    value='tab-1',
                    children=generate_tab_ethbtcusdt()
                ),
                dmc.TabsPanel(
                    id='tab-2',
                    value='tab-2',
                    children=generate_tab_basis_trade()
                ),
                dmc.TabsPanel(
                    id='tab-3',
                    value='tab-3',
                    children=generate_tab_short()
                )
            ],
        )
    ],
    style={"maxWidth": "1200px", "margin": "auto", "paddingTop": "50px"}
)


# Define the layout of the app
app_layout = html.Div(
    children=[
        html.Div(
            id='page-content',
            children=[
            page_layout
            ],
        )
    ],
    style={"maxWidth": "1200px", "margin": "auto", "paddingTop": "50px"}
)