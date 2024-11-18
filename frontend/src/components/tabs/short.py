from dash import dcc, html
from dash.dependencies import Input, Output


def generate_tab_short():

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