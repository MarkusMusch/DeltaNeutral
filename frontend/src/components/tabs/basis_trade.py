from dash import html, no_update
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc

from backend.models.models_orm import Symbol
from frontend.src.data_handling.data_handling_basis_trade import (
    generate_cumulative_funding_graph,
    generate_funding_rates_graph
)


def generate_tab_basis_trade() -> html.Div:
    """
    Generate the content for the Basis Trade tab.

    Returns:
        html.Div: The content to be rendered in the Basis Trade tab.
    """
    return html.Div(
        children=[
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        span=2.5,
                        children=[
                            dmc.Fieldset(
                                legend="Chart Settings",
                                mt='xl',
                                children=[
                                    dmc.Select(
                                        id="basis-trade-select-coin",
                                        label="Select Coin",
                                        placeholder="Select Coin",
                                        value=Symbol.BTCUSDT,
                                        data=[
                                            {"value": Symbol.BTCUSDT, "label": "BTC",
                                             "description": "Bitcoin"},
                                            {"value": Symbol.SOLUSDT, "label": "SOL",
                                             "description": "Solana"},
                                            {"value": Symbol.ETHUSDT, "label": "ETH",
                                             "description": "Ethereum"}
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    dmc.GridCol(
                        span=9.5,
                        children=[
                            dmc.Carousel(
                                id='basis-trade-carousel',
                                withIndicators=True,
                                classNames={"indicator": "dmc-indicator"},
                                loop=True,
                                children=[
                                    dmc.CarouselSlide(
                                        id='basis-trade-carousel-slide-1',
                                        children=[]
                                    ),
                                    dmc.CarouselSlide(
                                        id='basis-trade-carousel-slide-2',
                                        children=[]
                                    )
                                ]
                            )
                        ]
                    )
                ],
            )
        ]
    )


def register_callbacks_basis_trade(app):
    @app.callback(
        Output('basis-trade-carousel-slide-1', 'children', allow_duplicate=True),
        Output('basis-trade-carousel-slide-2', 'children', allow_duplicate=True),
        Input('tab-1', 'children'),
        Input('basis-trade-select-coin', 'value'),
        State('tab-1-store', 'data'),
        prevent_initial_call=True
    )
    def handle_tab_switch_basis_trade(children, coin, data):
        """ 
        Handle the tab switch event for the Basis Trade tab.
        
        Args:
            children (Any): The content of the Basis Trade tab.
            data (dict): The current state data stored in `tab-2-store`. It includes information 
                        like which slide is currently active.

        Returns:
            Tuple[Any, Any]: A tuple containing:
                - The updated content for `basis-trade-carousel-slide-1`.
                - The updated content for `basis-trade-carousel-slide-2`.
        """
        if data['active_carousel'] == 0:
            return generate_cumulative_funding_graph(coin), no_update
        elif data['active_carousel'] == 1:
            return no_update, generate_funding_rates_graph(coin)
        else:
            return no_update, no_update

    @app.callback(
        Output('basis-trade-carousel-slide-1', 'children', allow_duplicate=True),
        Output('basis-trade-carousel-slide-2', 'children', allow_duplicate=True),
        Output('tab-1-store', 'data'),
        Input('basis-trade-carousel', 'active'),
        State('tab-1-store', 'data'),
        State('basis-trade-select-coin', 'value'),
        prevent_initial_call=True
    )
    def update_basis_trade(active, data, coin):
        """
        Update the content of the slides in the basis trade carousel based on the active slide.

        Args:
            active (int): The index of the currently active slide in the `basis-trade-carousel`.
            data (dict): The current state data stored in `tab-2-store`. It includes information 
                        like which slide is currently active.

        Returns:
            Tuple[Any, Any, dict]: A tuple containing:
                - The updated content for `basis-trade-carousel-slide-1` if `active` is 0.
                - The updated content for `basis-trade-carousel-slide-2` if `active` is 1.
                - The updated state data reflecting the currently active carousel slide.
        """
        if active == 0:
            data['active_carousel'] = 0
            return generate_cumulative_funding_graph(coin), no_update, data
        elif active == 1:
            data['active_carousel'] = 1
            return no_update, generate_funding_rates_graph(coin), data
        else:
            return no_update, no_update, data

    @app.callback(
        Output('basis-trade-carousel-slide-2', 'children'),
        Input('basis-trade-carousel-slide-1', 'children'),
        State('basis-trade-select-coin', 'value'),
        prevent_initial_call=True
    )
    def update_basis_trade_carousel_slide_2(children, coin):
        """
        If Slide 1 has been updated, load the graph for slide 2

        Args:
            children (Any): The content of the first slide in the basis trade carousel.

        Returns:
            Any: The content to be rendered in the second slide, generated by the 
                `generate_funding_rates_graph()` function.
        """
        return generate_funding_rates_graph(coin)