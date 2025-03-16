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
                                html.Br(),
                                html.Div(
                                    id="air_quality_advice",
                                    className="text-center text-danger fw-bold",
                                ),  # ✅ เพิ่มข้อความแนะ
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
            # ✅ เพิ่มส่วนของ Input และ Output สำหรับพยากรณ์รายชั่วโมง
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Input Data", className="card-title"),
                                    dbc.Label("Humidity (%)"),
                                    dbc.Input(
                                        id="input_humidity",
                                        type="number",
                                        value=50,
                                        step=1,
                                        min=0,
                                        max=100,
                                    ),
                                    dbc.Label("Temperature (°C)"),
                                    dbc.Input(
                                        id="input_temperature",
                                        type="number",
                                        value=30,
                                        step=0.1,
                                    ),
                                    html.Br(),
                                    dbc.Button(
                                        "Predict Next 24 Hours",
                                        id="predict_hourly_btn",
                                        color="primary",
                                        className="mt-2 w-100",
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
                                    "PM2.5 Forecast (Next 24 Hours)",
                                    className="text-center",
                                ),
                                html.Div(id="hourly_prediction_table"),
                            ]
                        ),
                        width=8,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                dbc.Col(dcc.Graph(id="hourly_prediction_graph"), width=12),
            ),
        ],
    )
