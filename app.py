import dash
from dash import Input, Output, html
import dash_bootstrap_components as dbc
import plotly.express as px
from layout import get_layout
from data_processing import load_and_clean_data
from model import setup_model, predict_next_7_days, predict_next_24_hours

# ✅ โหลดข้อมูล
data = load_and_clean_data()
setup_model(data)  # ตั้งค่า PyCaret

# ✅ สร้างแอป Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = get_layout()


# ✅ Callback สำหรับพยากรณ์
@app.callback(
    [
        Output("latest_data", "children"),
        Output("prediction_table", "children"),
        Output("prediction_graph", "figure"),
        Output("air_quality_advice", "children"),
    ],
    [Input("predict_btn", "n_clicks")],
    prevent_initial_call=True,
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
    last_date = data.index[-1]

    # ✅ พยากรณ์ 7 วันข้างหน้า
    df_result = predict_next_7_days(latest_data, last_date)

    avg_pm25 = df_result["PM2.5 Prediction"].mean()

    if avg_pm25 <= 25:
        advice = "🌿 Air quality is **GOOD** this week. Enjoy outdoor activities!"
    elif avg_pm25 <= 50:
        advice = "😷 Air quality is **MODERATE**. Consider reducing outdoor activities."
    elif avg_pm25 <= 100:
        advice = "⚠️ Air quality is **UNHEALTHY** for sensitive groups. Wear a mask if necessary."
    else:
        advice = "🚨 Air quality is **VERY POOR**. Avoid going outside."

    # ✅ แสดงตาราง
    table = dbc.Table(
        [
            html.Thead(html.Tr([html.Th("Date"), html.Th("PM2.5 Prediction")])),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(row["Date"]),
                            html.Td(f"{row['PM2.5 Prediction']:.2f}"),
                        ]
                    )
                    for _, row in df_result.iterrows()
                ]
            ),
        ],
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
        advice,
    )


@app.callback(
    [
        Output("hourly_prediction_table", "children"),
        Output("hourly_prediction_graph", "figure"),
    ],
    [
        Input("predict_hourly_btn", "n_clicks"),
        Input("input_humidity", "value"),
        Input("input_temperature", "value"),
        Input("input_day", "value"),
        Input("input_month", "value"),
        Input("input_hour", "value"),
    ],
    prevent_initial_call=True,
)
def predict_hourly_pm25(n_clicks, humidity, temperature, day, month, hour):
    if n_clicks == 0:
        return "", px.line(title="PM2.5 Hourly Forecast")

    last_date = data.index[-1]

    # ✅ พยากรณ์ PM2.5 รายชั่วโมง
    df_result = predict_next_24_hours(humidity, temperature, day, month, hour)

    # ✅ แสดงตาราง
    table = dbc.Table(
        [
            html.Thead(html.Tr([html.Th("DateTime"), html.Th("PM2.5 Prediction")])),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(row["DateTime"]),
                            html.Td(f"{row['PM2.5 Prediction']:.2f}"),
                        ]
                    )
                    for _, row in df_result.iterrows()
                ]
            ),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        className="mt-3",
    )

    # ✅ สร้างกราฟ
    fig = px.line(
        df_result,
        x="DateTime",
        y="PM2.5 Prediction",
        markers=True,
        title="PM2.5 Hourly Forecast",
    )

    return table, fig


# ✅ รันเซิร์ฟเวอร์
if __name__ == "__main__":
    app.run_server(debug=True)
