import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
BINANCE_ETH_USDT_TICKER_SYMBOL = "ethusdt"