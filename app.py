import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pycaret.regression import setup, load_model, predict_model

# ✅ โหลดข้อมูลจากไฟล์ Excel
data = pd.read_excel("data/data.xlsx")

# ✅ แปลง timestamp เป็น datetime และสร้างฟีเจอร์ที่ใช้เทรน
data["timestamp"] = pd.to_datetime(data["timestamp"])
data["hour"] = data["timestamp"].dt.hour
data["day"] = data["timestamp"].dt.day
data["month"] = data["timestamp"].dt.month

# ✅ setup() เพื่อใช้กับ PyCaret
setup(
    data=data[["humidity", "temperature", "pm_2_5", "hour", "day", "month"]],
    target="pm_2_5",
    session_id=123,
    train_size=0.8,
    remove_outliers=True,
)

# ✅ โหลดโมเดลที่เทรนไว้
model = load_model("best_model")

# ✅ สร้างแอป Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ✅ Layout ของเว็บ
app.layout = dbc.Container(
    fluid=True,
    children=[
        # ✅ Navbar
        dbc.NavbarSimple(
            brand="PM2.5 Prediction Dashboard",
            brand_href="#",
            color="primary",
            dark=True,
            className="mb-4",
        ),
        # ✅ Input Section
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
                                "PM2.5 Forecast (Next 7 Days)", className="text-center"
                            ),
                            html.Div(id="prediction_table"),
                        ]
                    ),
                    width=8,
                ),
            ],
            className="mb-4",
        ),
        # ✅ Graph Section
        dbc.Row(
            dbc.Col(dcc.Graph(id="prediction_graph"), width=12),
        ),
    ],
)


# ✅ Callback สำหรับการพยากรณ์
@app.callback(
    [
        Output("latest_data", "children"),
        Output("prediction_table", "children"),
        Output("prediction_graph", "figure"),
    ],
    [Input("predict_btn", "n_clicks")],
)
def predict_pm25(n_clicks):
    if n_clicks == 0:
        latest = data.iloc[-1]
        return (
            f"Humidity: {latest['humidity']}, Temp: {latest['temperature']}",
            "",
            px.line(title="PM2.5 Forecast"),
        )

    # ✅ ใช้ข้อมูลล่าสุดจากไฟล์
    latest_data = data.iloc[-1]

    # ✅ พยากรณ์ 7 วันข้างหน้า
    future_pred = []
    future_dates = pd.date_range(start=pd.Timestamp.today(), periods=7, freq="D")

    for date in future_dates:
        input_data = pd.DataFrame(
            {
                "humidity": [latest_data["humidity"]],
                "temperature": [latest_data["temperature"]],
                "hour": [date.hour],
                "day": [date.day],
                "month": [date.month],
            }
        )

        pred = predict_model(model, data=input_data)
        next_day_pred = pred["prediction_label"][0]
        future_pred.append(next_day_pred)

    # ✅ สร้าง DataFrame สำหรับแสดงผล
    df_result = pd.DataFrame(
        {"Date": future_dates.strftime("%Y-%m-%d"), "PM2.5 Prediction": future_pred}
    )

    # ✅ สร้างตาราง
    table_header = [html.Thead(html.Tr([html.Th("Date"), html.Th("PM2.5 Prediction")]))]
    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [html.Td(row["Date"]), html.Td(f"{row['PM2.5 Prediction']:.2f}")]
                )
                for _, row in df_result.iterrows()
            ]
        )
    ]

    table = dbc.Table(
        table_header + table_body,
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        className="mt-3",
    )

    # ✅ สร้างกราฟ
    fig = px.line(
        df_result, x="Date", y="PM2.5 Prediction", markers=True, title="PM2.5 Forecast"
    )

    return (
        f"Humidity: {latest_data['humidity']}, Temp: {latest_data['temperature']}",
        table,
        fig,
    )


# ✅ รันเซิร์ฟเวอร์
if __name__ == "__main__":
    app.run_server(debug=True)
