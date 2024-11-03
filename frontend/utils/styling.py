import plotly.graph_objs as go


def create_dark_mode_layout(title):
    layout = go.Layout(
        title=title,
        plot_bgcolor='rgba(17, 17, 17, 1)',   # Plot background
        paper_bgcolor='rgba(17, 17, 17, 1)',  # Page background
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