import requests

api = "https://api.binance.com/api/v3/depth"

PARAMS = {
    "symbol": "ETHUSDT",
    "limit": 100
}

resp = requests.get(api, params=PARAMS)
print(resp.text)