import dash
from dash import Input, Output, html
import dash_bootstrap_components as dbc
import plotly.express as px
from layout import get_layout
from data_processing import load_data
from model import setup_model, predict_next_7_days

# ✅ โหลดข้อมูล
data = load_data()
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
    ],
    [Input("predict_btn", "n_clicks")],
)
def predict_pm25(n_clicks):
    if n_clicks == 0:
        latest = data.iloc[-1]
        return (
            f"Humidity: {latest['huminity']}, Temp: {latest['temperature']}",
            "",
            px.line(title="PM2.5 Forecast"),
        )

    # ✅ ใช้ข้อมูลล่าสุดจากไฟล์
    latest_data = data.iloc[-1]

    # ✅ พยากรณ์ 7 วันข้างหน้า
    df_result = predict_next_7_days(latest_data)

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
    )


# ✅ รันเซิร์ฟเวอร์
if __name__ == "__main__":
    app.run_server(debug=True)
