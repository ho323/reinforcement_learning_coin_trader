import time
import requests
import json
import csv
import pandas as pd
from datetime import datetime

ohlcv_path = ["data/btc_usdt_ohlcv_1m.csv", "data/btc_usdt_ohlcv_5m.csv", 
              "data/btc_usdt_ohlcv_1h.csv", "data/btc_usdt_ohlcv_4h.csv", 
              "data/btc_usdt_ohlcv_1d.csv", "data/btc_usdt_ohlcv_1w.csv"]

url = "https://api.binance.com/api/v3/klines"
interval = ["1m", "5m", "1h", "4h", "1d", "1w"]
symbol = "BTCUSDT"
limit = 1000

while True:
    for i in range(len(interval)):
        params = {"symbol": symbol, "interval": interval[i], "limit": limit}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = json.loads(response.content)
            with open(ohlcv_path[i], mode="a", newline="") as file:
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

        df = pd.read_csv(ohlcv_path[i])  # 중복된 행이 있는 csv 파일을 불러옵니다.
        df.drop_duplicates(["Timestamp"],inplace=True)  # 중복된 행을 제거합니다.
        df.to_csv(ohlcv_path[i], index=False)    # 결과를 새로운 csv 파일로 저장합니다.

    print(datetime.now(), " 수집 완료")

    time.sleep(3600)  # 1시간 대기