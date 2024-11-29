""" This module contains the content and callbacks for the Basis Trade tab. """
import dash_mantine_components as dmc

from backend.models.models_orm import Symbol
from frontend.src.components.components_id_tree import ComponentsIdTree


fieldset_basis_trade_leveraged = dmc.Fieldset(
    legend="Chart Settings Basis Trade Leveraged",
    mt='xl',
    children=[
        dmc.Select(
            id=ComponentsIdTree.Tabs.TabSettings.SELECT_COIN_BASIS_TRADE_LEVERAGED,
            label="Select Coin",
            placeholder="Select Coin",
            value=Symbol.BTCUSDT,
            data=[
                {"value": Symbol.BTCUSDT, "label": "BTC",
                    "description": "Bitcoin"},
                {"value": Symbol.SOLUSDT, "label": "SOL",
                    "description": "Solana"},
                {"value": Symbol.ETHUSDT, "label": "ETH",
                    "description": "Ethereum"}
            ]
        )
    ]
)