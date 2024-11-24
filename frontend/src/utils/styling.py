""" This module contains functions that help with styling the plots. """
import plotly.graph_objs as go


def create_dark_mode_layout(title):
    layout = go.Layout(
        title=title,
        plot_bgcolor='#242424',   # Plot background
        paper_bgcolor='#242424',  # Page background
        font=dict(color='white'),             # Text color
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='white',
            color='white',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='white',
            color='white',
        )
    )

    return layout