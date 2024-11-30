""" This module contains the layout and callbacks for the ETHBTCUSDT tab. """
from typing import List, Tuple

from dash import callback, dcc, no_update
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc

from frontend.src.components.components_id_tree import ComponentsIdTree
from frontend.src.components.graph_layout import generate_graph
from frontend.src.data_handling.data_handling_ethbtcusdt import (
    load_data_cumulative_arbitrage,
    load_data_funding_rates_ethbtcusdt,
    load_data_open_interest,
    load_data_cumulative_funding_ethbtcusdt
)


fieldset_ethbtcusdt = dmc.Fieldset(
    legend="Chart Settings ETHBTCUSDT Arbitrage",
    mt='xl',
    children=[]
)


@callback(
    Output(ComponentsIdTree.Tabs.TabCarousel.CAROUSEL_ETHBTCUSDT, 'children'),
    Input(ComponentsIdTree.Tabs.TabPanels.PANEL_ETHBTCUSDT, 'children'),
    State(ComponentsIdTree.Tabs.TabStores.STORE_ETHBTCUSDT, 'data'),
    prevent_initial_call=True
)
def handle_tab_switch_ethbtcusdt(
    _: dmc.Box,
    data: dict
) -> List[dmc.CarouselSlide]:
    """ 
    Handle the tab switch event for the ETHBTCUSDT tab.
    
    Args:
        children (Any): The content of the ETHBTCUSDT tab.
        data (dict): The current state data stored in `tab-1-store`. It includes information
                    like which slide is currently active.
                    
    Returns:
        List[dmc.CarouselSlide]: The updated content for the slides in the ETHBTCUSDT carousel.
    """
    if data['active_carousel'] in {0, 1, 2, 3}:

        carousel = [dmc.CarouselSlide([]) for _ in range(4)]
        funcs = [
            (load_data_cumulative_arbitrage, False),
            (load_data_funding_rates_ethbtcusdt, True),
            (load_data_open_interest, False),
            (load_data_cumulative_funding_ethbtcusdt, False)
        ]
        carousel[data['active_carousel']] = dmc.CarouselSlide(
            generate_graph(
                *funcs[data['active_carousel']][0](),
                funcs[data['active_carousel']][1])
        )

        return carousel
    else:
        return no_update


@callback(
    Output(ComponentsIdTree.Tabs.TabCarousel.CAROUSEL_ETHBTCUSDT, 'children', allow_duplicate=True),
    Output(ComponentsIdTree.Tabs.TabStores.STORE_ETHBTCUSDT, 'data'),
    Input(ComponentsIdTree.Tabs.TabCarousel.CAROUSEL_ETHBTCUSDT, 'active'),
    State(ComponentsIdTree.Tabs.TabStores.STORE_ETHBTCUSDT, 'data'),
    prevent_initial_call=True
)
def update_ethbtcusdt(
    active: int,
    data: dict
) -> Tuple[List[dmc.CarouselSlide], dcc.Store]:
    """
    Update the ETHBTCUSDT carousel based on the active slide.

    Args:
        active (int): The index of the currently active slide in the `ethbtcusdt-carousel`.
        data (dict): The current state data stored in `tab-1-store`. It includes information
                    like which slide is currently active.

    Returns:
        Tuple[List[dmc.CarouselSlide], dcc.Store]: A tuple containing:
            - The updated content for the ETHBTCUSDT carousel.
            - The updated state data stored in this tabs store.
    """
    if active in {0, 1, 2, 3}:
        data['active_carousel'] = active
    else:
        return no_update, data

    carousel = [dmc.CarouselSlide([]) for _ in range(4)]
    funcs = [
        (load_data_cumulative_arbitrage, False),
        (load_data_funding_rates_ethbtcusdt, True),
        (load_data_open_interest, False),
        (load_data_cumulative_funding_ethbtcusdt, False)
    ]
    carousel[data['active_carousel']] = dmc.CarouselSlide(
        generate_graph(
            *funcs[data['active_carousel']][0](),
            funcs[data['active_carousel']][1])
    )

    return carousel, data