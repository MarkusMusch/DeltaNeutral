""" Main file to run the Dash app """
from dash import callback, Dash, _dash_renderer, Input, Output, State 
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from sqlalchemy import create_engine

from backend.download_data import catch_latest_funding, catch_latest_open_interest, catch_latest_interest
from backend.models.models_orm import Base, Coin, Symbol
from frontend.src.layouts.page_layout import app_layout
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


theme_toggle = dmc.ActionIcon(
    id="color-scheme-toggle",
    variant="transparent",
    color="yellow",
    size="lg",
    ms="auto",
    children=[
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ]
)


app.layout = dmc.MantineProvider(
    id="mantine-provider",
    forceColorScheme='dark',
    children=[
        dmc.AppShell(
            children=[
                dmc.AppShellHeader(
                    children=[
                        dmc.Group(
                            align="right",
                            p="md",
                            pr="lg",
                            children=[
                                theme_toggle
                            ]
                        )
                    ]
                ),
                dmc.AppShellMain(
                    children=[
                        app_layout
                    ]
                ),
                dmc.AppShellFooter(
                    p="xs",
                    children=[
                        dmc.Text(
                            size="xs",
                            p="xxs",
                            children=[
                                "© 2024, None of the above is financial advice."
                            ]
                        )
                    ]
                )
            ],
            header={"height": "60px"},
            footer={"height": "40px"},
            p="xl",
            m="xl"
        )
    ]
)


register_callbacks_ethbtcusdt(app)


@callback(
    Output("mantine-provider", "forceColorScheme"),
    Input("color-scheme-toggle", "n_clicks"),
    State("mantine-provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def switch_theme(_, theme):
    return "dark" if theme == "light" else "light"


if __name__ == '__main__':
    app.run_server(debug=True)