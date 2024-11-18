""" Main file to run the Dash app """
from dash import Dash, _dash_renderer
import dash_mantine_components as dmc
from dash_mantine_components import MantineProvider
from sqlalchemy import create_engine

from backend.download_data import catch_latest_funding, catch_latest_open_interest, catch_latest_interest
from backend.models.models_orm import Base, Coin, Symbol
from frontend.src.layouts.page_layout import app_layout
from frontend.src.components.tabs.basis_trade import register_callbacks_basis_trade
from frontend.src.components.tabs.ethbtcusdt import register_callbacks_ethbtcusdt


engine = create_engine('sqlite:///funding_history.db')
Base.metadata.create_all(engine)


for symbol in Symbol:

    catch_latest_funding(symbol)
    catch_latest_open_interest(symbol)

for coin in Coin:

    catch_latest_interest(coin)

_dash_renderer._set_react_version("18.2.0")
app = Dash(__name__, external_stylesheets=[dmc.styles.CAROUSEL])

app.layout = MantineProvider(app_layout)

register_callbacks_basis_trade(app)
register_callbacks_ethbtcusdt(app)

if __name__ == '__main__':
    app.run_server(debug=True)