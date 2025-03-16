import pandas as pd


def load_and_clean_data(file_path="data/data.xlsx"):
    """โหลดข้อมูลจากไฟล์ Excel และคลีนข้อมูล"""
    data = pd.read_excel(file_path)

    # ✅ แปลง timestamp เป็น datetime
    data["timestamp"] = pd.to_datetime(data["timestamp"])

    # ✅ ดึงข้อมูลวัน ชั่วโมง เดือนจาก timestamp
    data["hour"] = data["timestamp"].dt.hour
    data["day"] = data["timestamp"].dt.day
    data["month"] = data["timestamp"].dt.month

    # ✅ ตั้งค่า timestamp เป็น index
    data.set_index("timestamp", inplace=True)

    return data
