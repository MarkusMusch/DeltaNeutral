from dash import dcc, html
from dash.dependencies import Input, Output

from dashboard.views.basis_trade import PageInfoBasisTrade, page_layout_basistrade
from dashboard.views.basis_trade_leveraged import PageInfoBasisTradeLeveraged, page_layout_basistrade_leveraged
from dashboard.views.ethbtcusdt import PageInfoETHBTCUSDT, page_layout_ethbtcusdt
from dashboard.views.short import PageInfoShort, page_layout_short


# Define the navigation bar using pure Dash components
navbar = html.Nav(
    children=[
        dcc.Link(PageInfoETHBTCUSDT.NAV_LINK.value,
                 href=PageInfoETHBTCUSDT.HREF.value,
                 className="nav-link", style={"padding": "10px", "color": "white", "textDecoration": "none"}),
        dcc.Link(PageInfoBasisTrade.NAV_LINK.value,
                 href=PageInfoBasisTrade.HREF.value,
                 className="nav-link", style={"padding": "10px", "color": "white", "textDecoration": "none"}),
        dcc.Link(PageInfoBasisTradeLeveraged.NAV_LINK.value,
                 href=PageInfoBasisTradeLeveraged.HREF.value,
                 className="nav-link", style={"padding": "10px", "color": "white", "testDecoration": "none"}),
        dcc.Link(PageInfoShort.NAV_LINK.value,
                 href=PageInfoShort.HREF.value,
                 className="nav-link", style={"padding": "10px", "color": "white", "textDecoration": "none"})
    ],
    style={
        "display": "flex",
        "flexDirection": "column",  # Stack items vertically
        "alignItems": "center",     # Center items horizontally
        "justifyContent": "center", # Center items vertically
        "position": "fixed",        # Fix the navbar to the left side
        "left": "0",
        "top": "0",
        "height": "100vh",          # Take full height of the viewport
        "width": "150px",           # Set a fixed width for the navbar
        "backgroundColor": "#007bff",
    }
)


# Define the layout of the app
app_layout = html.Div(
    children=[
        navbar,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content',
                 children=[
                    page_layout_ethbtcusdt,
                    page_layout_basistrade,
                    page_layout_basistrade_leveraged,
                    page_layout_short
                 ],
            )
    ],
    style={"maxWidth": "1200px", "margin": "auto", "paddingTop": "50px"}
)

def register_callbacks(app):
    @app.callback(
            Output('page-content', 'children'),
            Input('url', 'pathname')
    )
    def render_page(pathname):
        if pathname == PageInfoETHBTCUSDT.HREF.value:
            return page_layout_ethbtcusdt
        elif pathname == PageInfoBasisTrade.HREF.value:
            return page_layout_basistrade
        elif pathname == PageInfoBasisTradeLeveraged.HREF.value:
            return page_layout_basistrade_leveraged
        elif pathname == PageInfoShort.HREF.value:
            return page_layout_short