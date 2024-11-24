""" This module contains the layout and callbacks for the ETHBTCUSDT tab. """
from dash import html, no_update
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc

from frontend.src.data_handling.data_handling_ethbtcusdt import (
    generate_cumulative_arbitrage_graph,
    generate_cumulative_funding_rates_graph,
    generate_funding_rates_graph,
    generate_open_interest_graph
)


def generate_tab_ethbtcusdt() -> html.Div:
    """ Generate the content for the ETHBTCUSDT tab.

    Returns:
        html.Div: The content for the ETHBTCUSDT tab.
    """
    return html.Div(
        children=[
            dmc.Carousel(
                id='ethbtcusdt-carousel',
                withIndicators=True,
                classNames={"indicator": "dmc-indicator"},
                loop=True,
                children=[
                    dmc.CarouselSlide(
                        id='ethbtcusdt-carousel-slide-1',
                        children=generate_cumulative_arbitrage_graph()
                    ),
                    dmc.CarouselSlide(
                        id='ethbtcusdt-carousel-slide-2',
                        children=[]
                        
                    ),
                    dmc.CarouselSlide(
                        id='ethbtcusdt-carousel-slide-3',
                        children=[]
                    ),
                    dmc.CarouselSlide(
                        id='ethbtcusdt-carousel-slide-4',
                        children=[]
                    )
                ]
            )
        ],
        style={"backgroundColor": "#111111"}
    )


def register_callbacks_ethbtcusdt(app):
    @app.callback(
        Output('ethbtcusdt-carousel-slide-1', 'children', allow_duplicate=True),
        Output('ethbtcusdt-carousel-slide-2', 'children', allow_duplicate=True),
        Output('ethbtcusdt-carousel-slide-3', 'children', allow_duplicate=True),
        Output('ethbtcusdt-carousel-slide-4', 'children', allow_duplicate=True),
        Input('tab-3', 'children'),
        State('tab-3-store', 'data'),
        prevent_initial_call=True
    )
    def handle_tab_switch_ethbtcusdt(_, data):
        """ 
        Handle the tab switch event for the ETHBTCUSDT tab.
        
        Args:
            children (Any): The content of the ETHBTCUSDT tab.
            data (dict): The current state data stored in `tab-1-store`. It includes information
                        like which slide is currently active.
                        
        Returns:
            Tuple[Any, Any, Any, Any]: A tuple containing:
                - The updated content for `ethbtcusdt-carousel-slide-1`.
                - The updated content for `ethbtcusdt-carousel-slide-2`.
                - The updated content for `ethbtcusdt-carousel-slide-3`.
                - The updated content for `ethbtcusdt-carousel-slide-4`.
        """
        if data['active_carousel'] == 0:
            return generate_cumulative_arbitrage_graph(), no_update, no_update, no_update
        elif data['active_carousel'] == 1:
            return no_update, generate_funding_rates_graph(), no_update, no_update
        elif data['active_carousel'] == 2:
            return no_update, no_update, generate_open_interest_graph(), no_update
        elif data['active_carousel'] == 3:
            return no_update, no_update, no_update, generate_cumulative_funding_rates_graph()
        else:
            return no_update, no_update, no_update, no_update

    @app.callback(
        Output('ethbtcusdt-carousel-slide-1', 'children', allow_duplicate=True),
        Output('ethbtcusdt-carousel-slide-2', 'children', allow_duplicate=True),
        Output('ethbtcusdt-carousel-slide-3', 'children', allow_duplicate=True),
        Output('ethbtcusdt-carousel-slide-4', 'children', allow_duplicate=True),
        Output('tab-3-store', 'data'),
        Input('ethbtcusdt-carousel', 'active'),
        State('tab-3-store', 'data'),
        prevent_initial_call=True
    )
    def update_ethbtcusdt(active, data):
        """
        Update the ETHBTCUSDT carousel based on the active slide.

        Args:
            active (int): The index of the currently active slide in the `ethbtcusdt-carousel`.
            data (dict): The current state data stored in `tab-1-store`. It includes information
                        like which slide is currently active.

        Returns:
            Tuple[Any, Any, Any, Any, dict]: A tuple containing:
                - The updated content for `ethbtcusdt-carousel-slide-1` if `active` is 0.
                - The updated content for `ethbtcusdt-carousel-slide-2` if `active` is 1.
                - The updated content for `ethbtcusdt-carousel-slide-3` if `active` is 2.
                - The updated content for `ethbtcusdt-carousel-slide-4` if `active` is 3.
                - The updated state data reflecting the currently active carousel slide.
        """
        if active == 0:
            data['active_carousel'] = 0
            return generate_cumulative_arbitrage_graph(), no_update, no_update, no_update, data
        elif active == 1:
            data['active_carousel'] = 1
            return no_update, generate_funding_rates_graph(), no_update, no_update, data
        elif active == 2:
            data['active_carousel'] = 2
            return no_update, no_update, generate_open_interest_graph(), no_update, data
        elif active == 3:
            data['active_carousel'] = 3
            return no_update, no_update, no_update, generate_cumulative_funding_rates_graph(), data
        else:
            return no_update, no_update, no_update, no_update, data

    # If Slide 1 has been updated, load the graph for slide 2 
    @app.callback(
        Output('ethbtcusdt-carousel-slide-2', 'children'),
        Input('ethbtcusdt-carousel-slide-1', 'children'),
        prevent_initial_call=True
    )
    def update_ethbtcusdt_carousel_slide_2(_):
        """ If Slide 1 has been updated, load the graph for slide 2

        Args:
            children (Any): The content of the first slide in the ETHBTCUSDT carousel.

        Returns:
            Any: The updated content for `ethbtcusdt-carousel-slide-2`.
        """
        return generate_funding_rates_graph()
    
    # If Slide 1 has been updated, load the graph for slide 4
    @app.callback(
        Output('ethbtcusdt-carousel-slide-4', 'children'),
        Input('ethbtcusdt-carousel-slide-1', 'children'),
        prevent_initial_call=True
    )
    def update_ethbtcusdt_carousel_slide_4(_):
        """ If Slide 1 has been updated, load the graph for slide 4
        
        Args:
            children (Any): The content of the first slide in the ETHBTCUSDT carousel.
            
        Returns:
            Any: The updated content for `ethbtcusdt-carousel-slide-4`.
        """
        return generate_cumulative_funding_rates_graph()
    
    # If Slide 2 or Slide 4 has been updated, load the graph for slide 3
    @app.callback(
        Output('ethbtcusdt-carousel-slide-3', 'children'),
        Input('ethbtcusdt-carousel-slide-2', 'children'),
        Input('ethbtcusdt-carousel-slide-4', 'children'),
        prevent_initial_call=True
    )
    def update_ethbtcusdt_carousel_slide_3(_, _2):
        """ If Slide 2 or Slide 4 has been updated, load the graph for slide 3 
        
        Args:
            children (Any): The content of the second slide in the ETHBTCUSDT carousel.
            children2 (Any): The content of the fourth slide in the ETHBTCUSDT carousel.
        
        Returns:
            Any: The updated content for `ethbtcusdt-carousel-slide-3`.
        """
        return generate_open_interest_graph()