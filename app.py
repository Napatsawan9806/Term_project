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


@app.callback(
    [
        Output("prediction_table", "children"),
        Output("prediction_graph", "figure"),
    ],
    [Input("predict_btn", "n_clicks")],
    [State("latest_data", "data")],
)
def predict_pm25_weekly(n_clicks, latest_data):
    if n_clicks is None:
        return "", px.line(title="PM2.5 Forecast (Next 7 Days)")

    # ✅ ดึงข้อมูลล่าสุด
    latest_data = pd.DataFrame(latest_data, index=[0])
    last_date = pd.Timestamp.now()

    # ✅ สร้างช่วงเวลา 168 ชั่วโมงข้างหน้า (7 วัน × 24 ชั่วโมง)
    future_dates = pd.date_range(start=last_date, periods=168, freq="H")

    # ✅ สร้าง DataFrame สำหรับโมเดล
    input_data = pd.DataFrame(
        {
            "humidity": [latest_data["humidity"].iloc[0]] * 168,
            "temperature": [latest_data["temperature"].iloc[0]] * 168,
            "hour": future_dates.hour,
            "day": future_dates.day,
            "month": future_dates.month,
        }
    )

    # ✅ ใช้โมเดลพยากรณ์
    predictions = predict_model(model, data=input_data)
    input_data["PM2.5 Prediction"] = predictions["prediction_label"]
    input_data["DateTime"] = future_dates

    # ✅ สร้างค่าเฉลี่ยรายวัน
    daily_avg = input_data.resample("D", on="DateTime").mean()

    # ✅ แสดงผลในตาราง (เฉพาะค่าเฉลี่ยรายวัน)
    table = dbc.Table(
        [
            html.Thead(html.Tr([html.Th("Date"), html.Th("PM2.5 Prediction (Avg)")])),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(row["DateTime"].strftime("%Y-%m-%d")),
                            html.Td(f"{row['PM2.5 Prediction']:.2f}"),
                        ]
                    )
                    for _, row in daily_avg.iterrows()
                ]
            ),
        ],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        className="mt-3",
    )

    # ✅ สร้างกราฟ (รองรับการซูมดูรายชั่วโมง)
    fig = px.line(
        input_data,
        x="DateTime",
        y="PM2.5 Prediction",
        title="PM2.5 Forecast (Next 7 Days)",
        labels={"DateTime": "Date", "PM2.5 Prediction": "PM2.5 Level"},
    )
    fig.update_xaxes(rangeslider_visible=True)  # ✅ เปิดใช้งาน Range Slider
    fig.update_traces(line=dict(width=1))  # ✅ ปรับเส้นให้บางเพื่อดูแนวโน้ม

    return table, fig


@app.callback(
    [
        Output("hourly_prediction_table", "children"),
        Output("hourly_prediction_graph", "figure"),
    ],
    [
        Input("predict_hourly_btn", "n_clicks"),
        Input("input_humidity", "value"),
        Input("input_temperature", "value"),
    ],
)
def predict_hourly_pm25(n_clicks, humidity, temperature):
    if n_clicks == 0:
        return "", px.line(title="PM2.5 Hourly Forecast")

    last_date = data.index[-1]

    # ✅ พยากรณ์ PM2.5 รายชั่วโมง
    df_result = predict_next_24_hours(humidity, temperature, last_date)

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
