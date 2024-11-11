import time
import requests

api = "https://api.binance.com/api/v3/klines"

now = int(time.time() * 1000)

PARAMS = {
    "symbol": "ETHUSDT",
    "interval": '1s',
    "startTime": 1731318445000,
    "endTime": 1731318447000,
    "limit": 5
}

resp = requests.get(api, params=PARAMS)
print(resp.text)