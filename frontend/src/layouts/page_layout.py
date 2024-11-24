""" This module contains the layout of the page. """
from enum import Enum
from dash import dcc, html
import dash_mantine_components as dmc

from frontend.src.components.tabs.basis_trade import generate_tab_basis_trade
from frontend.src.components.tabs.basis_trade_leveraged import generate_tab_basis_trade_leveraged
from frontend.src.components.tabs.ethbtcusdt import generate_tab_ethbtcusdt
from frontend.src.components.tabs.short import generate_tab_short


class PageIds(Enum):
    TAB_ONE = 'page-one-tabs'


page_layout = dmc.Box(
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
                            children='Basis Trade'
                        ),
                        dcc.Store(
                            id='tab-2-store',
                            data={'active_carousel': 0}
                        ),
                        dmc.TabsTab(
                            value='tab-2',
                            children="Basis Trade Leveraged",
                        ),
                        dcc.Store(
                            id='tab-3-store',
                            data={'active_carousel': 0}
                        ),
                        dmc.TabsTab(
                            value='tab-3',
                            children="Arbitrage ETHBTCUSDT",
                        ),
                        dmc.TabsTab(
                            value='tab-4',
                            children="Short",
                        )
                    ]
                ),
                dmc.TabsPanel(
                    id='tab-1',
                    value='tab-1',
                    children=generate_tab_basis_trade()
                ),
                dmc.TabsPanel(
                    id='tab-2',
                    value='tab-2',
                    children=generate_tab_basis_trade_leveraged()
                ),
                dmc.TabsPanel(
                    id='tab-3',
                    value='tab-3',
                    children=generate_tab_ethbtcusdt()
                ),
                dmc.TabsPanel(
                    id='tab-4',
                    value='tab-4',
                    children=generate_tab_short()
                )
            ],
        )
    ],
    style={"maxWidth": "1600px", "margin": "auto"}
)


# Define the layout of the app
app_layout = dmc.Box(
    children=[
        dmc.Box(
            id='page-content',
            children=[
            page_layout
            ],
        )
    ],
    style={"paddingTop": "50px", "paddingLeft": "50px", "paddingRight": "50px"}
)