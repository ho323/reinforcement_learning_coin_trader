import time
import requests
import json
import csv
from datetime import datetime

url = "https://api.binance.com/api/v3/klines"
interval = "5m"
symbol = "BTCUSDT"
limit = 1  # 5분봉 데이터를 하나씩 가져옴

while True:
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = json.loads(response.content)
        with open("btc_usdt_ohlcv.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            for item in data:
                timestamp = item[0] / 1000  # 밀리초를 초 단위로 변환
                dt_object = datetime.fromtimestamp(timestamp)
                dt_str = dt_object.strftime("%Y-%m-%d %H:%M")
                open_price = float(item[1])
                high_price = float(item[2])
                low_price = float(item[3])
                close_price = float(item[4])
                volume = float(item[5])
                writer.writerow([dt_str, open_price, high_price, low_price, close_price, volume])
    else:
        print("Error:", response.status_code)

    time.sleep(300)  # 5분 대기