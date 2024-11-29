""" This module contains the layout and callbacks for the ETHBTCUSDT tab. """
from typing import List, Tuple, Union

from dash import callback, dcc, no_update
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc

from frontend.src.components.components_id_tree import ComponentsIdTree
from frontend.src.data_handling.data_handling_ethbtcusdt import (
    generate_graph_cumulative_arbitrage,
    generate_graph_cumulative_funding_rates,
    generate_graph_funding_rates,
    generate_graph_open_interest
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
        return [dmc.CarouselSlide(func()) for func in [
            generate_graph_cumulative_arbitrage,
            generate_graph_funding_rates,
            generate_graph_open_interest,
            generate_graph_cumulative_funding_rates
        ]]
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

    return [dmc.CarouselSlide(func()) for func in [
        generate_graph_cumulative_arbitrage,
        generate_graph_funding_rates,
        generate_graph_open_interest,
        generate_graph_cumulative_funding_rates
    ]], data