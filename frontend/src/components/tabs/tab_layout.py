from typing import Union

import dash_mantine_components as dmc


def generate_tab(
    id: Union[str, dict],
    fieldset: dmc.Fieldset
) -> dmc.Box:
    """ """
    return dmc.Box(
        children=[
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        span=2.5,
                        children=[fieldset]
                    ),
                    dmc.GridCol(
                        span=9.5,
                        children=[
                            dmc.Carousel(
                                id=id,
                                withIndicators=True,
                                classNames={"indicator": "dmc-indicator"},
                                loop=True
                            )
                        ]
                    )
                ]
            )
        ]
    )