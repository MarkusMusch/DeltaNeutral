from dash import Dash
from sqlalchemy import create_engine

from frontend.views.basis_trade import register_basistrade_callbacks
from frontend.views.basis_trade_leveraged import register_basistrade_leveraged_callbacks
from frontend.views.ethbtcusdt import register_ethbtcusdt_callbacks
from frontend.views.short import register_short_callbacks
from frontend.page_layout import app_layout, register_callbacks
from backend.download_data import catch_latest_funding, catch_latest_open_interest, catch_latest_interest
from backend.models.models_orm import Base, Coin, Symbol


engine = create_engine('sqlite:///funding_history.db')
Base.metadata.create_all(engine)


for symbol in Symbol:

    catch_latest_funding(symbol)
    catch_latest_open_interest(symbol)

for coin in Coin:

    catch_latest_interest(coin)


app = Dash(__name__)

app.layout = app_layout

# Register callbacks
register_callbacks(app)
register_basistrade_callbacks(app)
register_basistrade_leveraged_callbacks(app)
register_short_callbacks(app)
register_ethbtcusdt_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)