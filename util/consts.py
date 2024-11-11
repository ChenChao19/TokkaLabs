import os

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_NAME_TRANSACTION = "transactions"
REDIS_BINANCE_SPOT_DATA = "binance_spot_data"
REDIS_CHANNEL_TRANSACTION = "transaction_channel"

BINANCE_ETH_USDT_TICKER_SYMBOL = "ethusdt"
BINANCE_ETH_USDT_TICKER_SYMBOL_CAP = "ETHUSDT"
ETHERSCAN_API_KEY = "ETHERSCAN_API_KEY"
UNISWAP_V3_ETH_USDC_POOL_ADDR = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
ETH_BUFFER_BLOCK = 32
