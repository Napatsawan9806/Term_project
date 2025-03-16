import pandas as pd


def load_data(file_path="data/data.xlsx"):
    data = pd.read_excel(file_path)
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["hour"] = data["timestamp"].dt.hour
    data["day"] = data["timestamp"].dt.day
    data["month"] = data["timestamp"].dt.month
    return data
