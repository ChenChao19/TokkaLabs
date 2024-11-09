import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print("Trade update:", data)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")

# Connect to Binance WebSocket for BTC/USDT trade updates
ws = websocket.WebSocketApp(
    "wss://stream.binance.com:9443/ws/ethusdt@kline_1s",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)
ws.on_open = on_open
ws.run_forever()
