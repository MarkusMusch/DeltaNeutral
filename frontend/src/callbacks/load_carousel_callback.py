""" Callbacks for loading the content of the carousel in the basis trade and leveraged basis trade tabs. """
from typing import List, Tuple

from dash import callback, dcc, Input, MATCH, no_update, Output, State
import dash_mantine_components as dmc

from backend.models.models_orm import Symbol
from frontend.src.components.graph_layout import generate_graph
from frontend.src.data_handling.data_handling_basis_trade import (
    load_data_cumulative_funding,
    load_data_funding_rates
)
from frontend.src.data_handling.data_handling_basis_trade_leveraged import (
    load_data_cumulative_funding_leveraged,
    load_data_funding_rates_leveraged,
    load_data_net_income_leveraged
)


def generate_carousel_strategy(
    triggered: str,
    coin: Symbol,
    active: int,
    data: dict
) -> Tuple[List[dmc.CarouselSlide], dict]:
    """Generate the content for the carousel in the basis trade and leveraged basis trade tabs.
    
    Args:
        triggered (str): The type of the component that triggered the callback.
        coin (Symbol): The symbol of the coin selected in the Select component.
        active (int): The index of the currently active slide in the carousel.
        data (dict): The current state data stored in the store belonging to the active tab. It includes information
        
    Returns:
        List[dmc.CarouselSlide]: The content for the carousel.
    """
    if triggered == 'regular':
        if active == 0:
            data['active_carousel'] = 0
            return [
                dmc.CarouselSlide(
                    generate_graph(
                        *load_data_cumulative_funding(coin),
                        False
                    )
                ),
                dmc.CarouselSlide([])
            ], data
        elif active == 1:
            data['active_carousel'] = 1
            return [
                dmc.CarouselSlide([]),
                dmc.CarouselSlide(
                    generate_graph(
                        *load_data_funding_rates(coin)
                    )
                )
            ], data

    elif triggered == 'leveraged':
        if active == 0:
            data['active_carousel'] = 0
            return [
                dmc.CarouselSlide(
                    generate_graph(
                        *load_data_cumulative_funding_leveraged(coin)
                    )
                ),
                dmc.CarouselSlide([]),
                dmc.CarouselSlide([])
            ], data
        elif active == 1:
            data['active_carousel'] = 1
            return [
                dmc.CarouselSlide([]),
                dmc.CarouselSlide(
                    generate_graph(
                        *load_data_funding_rates_leveraged(coin)
                    )
                ),
                dmc.CarouselSlide([])
            ], data
        elif active == 2:
            data['active_carousel'] = 2
            return [
                dmc.CarouselSlide([]),
                dmc.CarouselSlide([]),
                dmc.CarouselSlide(
                    generate_graph(
                        *load_data_net_income_leveraged(coin)
                    )
                )
            ], data

    return no_update, data


@callback(
    Output({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'children', allow_duplicate=True),
    Output({"branch": "stores", "leaf": "basis-trade", "type": MATCH}, 'data'),
    Input({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'active'),
    State({"branch": "stores", "leaf": "basis-trade", "type": MATCH}, 'data'),
    State({"leaf": "select-coin", "leaf": "basis-trade", "type": MATCH}, 'value'),
    State({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'id'),
    prevent_initial_call=True
)
def update_basis_trade(
    active: int,
    data: dict,
    coin: Symbol,
    _id: str
) -> Tuple[List[dmc.CarouselSlide], dcc.Store]:
    """
    Update the content of the slides in the basis trade and leveraged basis trade carousel based on the active slide.

    Args:
        active (int): The index of the currently active slide in the carousel.
        data (dict): The current state data stored in the store belonging to the active tab. It includes information 
                    like which slide is currently active.
        coin (Symbol): The symbol of the coin selected in the Select component.
        _id (str): The ID of the component that triggered the callback.

    Returns:
        Tuple[Any, Any, dict]: A tuple containing:
            - The updated content for the carousel.
            - The updated state data reflecting the currently active carousel slide.
    """
    triggered = _id['type']
            
    return generate_carousel_strategy(triggered, coin, active, data)


@callback(
    Output({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'children', allow_duplicate=True),
    Input({"leaf": "select-coin", "leaf": "basis-trade", "type": MATCH}, 'value'),
    State({"branch": "stores", "leaf": "basis-trade", "type": MATCH}, 'data'),
    State({"branch": "carousel", "leaf": "basis-trade", "type": MATCH}, 'id'),
    prevent_initial_call=True
)
def handle_tab_switch_basis_trade(
    coin: Symbol,
    data: dict,
    _id: dict
) -> List[dmc.CarouselSlide]:
    """ 
    Handle the tab switch event for the Basis Trade tab.
 
    Args:
        _ (Any): The content of the Basis Trade tab.
        coin (Symbol): The symbol of the coin selected in the `basis-trade-leveraged-select-coin` component.
        data (dict): The current state data stored in `tab-2-store`. It includes information 
                    like which slide is currently active.
        _id (dict): The ID of the component that triggered the callback

    Returns:
        List[dmc.CarouselSlide]: The updated content for the slides in the Basis Trade carousel.
    """
    trigger = _id['type']

    if trigger == 'regular':
        carousel = [dmc.CarouselSlide([]) for _ in range(2)]
        loaders = [
            (load_data_cumulative_funding, False),
            (load_data_funding_rates, True)
        ]
        carousel[data["active_carousel"]] = dmc.CarouselSlide(
            generate_graph(
                *loaders[data["active_carousel"]][0](coin),
                loaders[data["active_carousel"]][1]
            )
        )
    elif trigger == 'leveraged':
        carousel = [dmc.CarouselSlide([]) for _ in range(3)]
        loaders = [
            load_data_cumulative_funding_leveraged,
            load_data_funding_rates_leveraged,
            load_data_net_income_leveraged
        ]
        carousel[data["active_carousel"]] = dmc.CarouselSlide(
            generate_graph(
                *loaders[data["active_carousel"]](coin)
            )
        )
        return carousel
    else:
        return no_update