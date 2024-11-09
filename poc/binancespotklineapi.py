import time
import requests

api = "https://api.binance.com/api/v3/klines"

now = int(time.time() * 1000)

PARAMS = {
    "symbol": "ETHUSDT",
    "interval": '1m',
    "startTime": now - 300000,
    "endTime": now
}

resp = requests.get(api, params=PARAMS)
print(resp.text)