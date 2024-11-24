""" This module contains the layout for the short tab. """
from dash import html


def generate_tab_short() -> html.Div:
    """ This function generates the layout for the short tab. 
    
    Returns:
        html.Div: A Dash div object that contains the layout for the short tab.
    """
    return html.Div(
        children=[
            html.H3(f'Graphical depiction of the trade over time.', style={'textAlign': 'center', 'color': 'white'}),
            html.Div([
                html.P(f'This page will show plots of the Short Trade', style={'color': 'white'})
            ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '4px', 'backgroundColor': '#222222'})
        ],
    )