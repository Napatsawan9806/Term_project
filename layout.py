import dash_bootstrap_components as dbc
from dash import html, dcc


def get_layout():
    return dbc.Container(
        fluid=True,
        children=[
            dbc.NavbarSimple(
                brand="PM2.5 Prediction Dashboard",
                brand_href="#",
                color="dark",
                dark=True,
                className="mb-4 shadow-sm rounded-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Latest Data from File",
                                        className="card-title text-primary fw-bold",
                                    ),
                                    html.Div(
                                        id="latest_data",
                                        className="mb-3 fs-5 fw-semibold text-secondary",
                                    ),
                                    dbc.Button(
                                        "Predict Next 7 Days",
                                        id="predict_btn",
                                        color="info",
                                        className="w-100 fw-bold",
                                    ),
                                ]
                            ),
                            className="shadow-lg rounded-4 border-0 p-3",
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
                className="mb-3",
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id="air_quality_advice",
                        className="mt-3 text-center text-warning fw-bold fs-5",
                    ),
                    width=12,
                ),
                className="mb-4",
            ),
            html.Div(
                [
                    html.H2("Input Data", className="text-primary mb-3"),
                    html.Label("Humidity (%)"),
                    dcc.Input(
                        id="input_humidity",
                        type="number",
                        value=70,
                        className="form-control mb-2",
                    ),
                    html.Label("Temperature (°C)"),
                    dcc.Input(
                        id="input_temperature",
                        type="number",
                        value=28,
                        className="form-control mb-2",
                    ),
                    html.Label("Select Day"),
                    dcc.Dropdown(
                        id="input_day",
                        options=[{"label": str(i), "value": i} for i in range(1, 32)],
                        value=1,
                        className="mb-2",
                    ),
                    html.Label("Select Month"),
                    dcc.Dropdown(
                        id="input_month",
                        options=[{"label": f"{i}", "value": i} for i in range(1, 13)],
                        value=1,
                        className="mb-2",
                    ),
                    html.Label("Select Hour"),
                    dcc.Dropdown(
                        id="input_hour",
                        options=[{"label": f"{i}:00", "value": i} for i in range(24)],
                        value=12,
                        className="mb-2",
                    ),
                    dbc.Button(
                        "Predict Next 24 Hours",
                        id="predict_hourly_btn",
                        color="primary",
                        className="mt-2",
                    ),
                    html.Div(id="hourly_prediction_table", className="mt-4"),
                    dcc.Graph(id="hourly_prediction_graph"),
                ],
                className="p-4 border rounded-3 shadow-sm mt-4",
            ),
        ],
    )
