import dash_bootstrap_components as dbc
from dash import html, dcc


def get_layout():
    return dbc.Container(
        fluid=True,
        children=[
            dbc.NavbarSimple(
                brand="PM2.5 Prediction Dashboard",
                brand_href="#",
                color="primary",
                dark=True,
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Latest Data from File", className="card-title"
                                    ),
                                    html.Div(id="latest_data", className="mb-3"),
                                    dbc.Button(
                                        "Predict Next 7 Days",
                                        id="predict_btn",
                                        color="primary",
                                        className="w-100",
                                    ),
                                ]
                            )
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Spinner(
                            [
                                html.H5(
                                    "PM2.5 Forecast (Next 7 Days)",
                                    className="text-center",
                                ),
                                html.Div(id="prediction_table"),
                            ]
                        ),
                        width=8,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                dbc.Col(dcc.Graph(id="prediction_graph"), width=12),
            ),
        ],
    )
