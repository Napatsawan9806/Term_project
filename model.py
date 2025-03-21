from pycaret.regression import setup, load_model, predict_model
import pandas as pd

data = pd.read_excel("data\data.xlsx")

# ✅ โหลดโมเดลที่เทรนไว้
model = load_model("best_model")


def setup_model(data):
    setup(
        data=data[["humidity", "temperature", "pm_2_5", "hour", "day", "month"]],
        target="pm_2_5",
        session_id=123,
        train_size=0.8,
        remove_outliers=True,
    )


def predict_next_7_days(latest_data, last_date):
    future_pred = []
    future_dates = pd.date_range(start=last_date, periods=8, freq="D")[1:]

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

    return pd.DataFrame(
        {"Date": future_dates.strftime("%Y-%m-%d"), "PM2.5 Prediction": future_pred}
    )


def predict_next_24_hours(humidity, temperature, day, month, hour):
    """พยากรณ์ค่า PM2.5 รายชั่วโมงจากค่าที่ผู้ใช้กรอก"""
    future_pred = []
    start_date = pd.Timestamp(
        year=2025, month=month, day=day, hour=hour
    )  # กำหนดเริ่มต้นจากค่าผู้ใช้
    future_dates = pd.date_range(start=start_date, periods=24, freq="H")

    for date in future_dates:
        input_data = pd.DataFrame(
            {
                "humidity": [humidity],
                "temperature": [temperature],
                "hour": [date.hour],
                "day": [date.day],
                "month": [date.month],
            }
        )

        pred = predict_model(model, data=input_data)
        next_hour_pred = pred["prediction_label"][0]
        future_pred.append(next_hour_pred)

    return pd.DataFrame(
        {
            "DateTime": future_dates.strftime("%Y-%m-%d %H:%M"),
            "PM2.5 Prediction": future_pred,
        }
    )
