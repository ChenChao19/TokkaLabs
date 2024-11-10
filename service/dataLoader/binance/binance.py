import logging
import asyncio
from client.AsyncBinanceWebsocketClient import AbstractBinanceWebSocketClient
from client.AsyncRedisClient import RedisClient
from service.dataLoader.BaseDataLoader import BaseLoader
from util.consts import BINANCE_ETH_USDT_TICKER_SYMBOL, REDIS_BINANCE_SPOT_DATA

class BinanceTickerClient(AbstractBinanceWebSocketClient):
    def __init__(self, symbol: str):
        super().__init__(symbol)
        self.redis = RedisClient()
        self.stop = False

    async def process_message(self, data):
        try:
            logging.info(f"Processing data for {self.symbol.upper()}: {data}")
            await self.redis.hset_json(REDIS_BINANCE_SPOT_DATA, int(data['E']/1000), round(float(data['c']), 2))
            logging.info(f"Stored price {round(float(data['c']), 2)} for event time {int(data['E']/1000)} in Redis.")
        except Exception as e:
            logging.error(f"Failed to store data in Redis: {e}")

    async def connect_forever(self):
        """Maintains a single, persistent connection with reconnection attempts if disconnected."""
        while not self.stop:
            try:
                logging.info(f"Connecting to Binance WebSocket for symbol: {self.symbol}")
                await self.connect()  # Connect once, handle reconnect within `connect`
            except Exception as e:
                logging.error(f"WebSocket connection error: {e}")
                await asyncio.sleep(5)  # Small delay before retrying
            if self.stop:
                break

    def shutdown(self):
        """Stops the persistent connection."""
        self.stop = True
        logging.info("Shutdown signal received, stopping BinanceTickerClient...")

class BinanceLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.binance_client = BinanceTickerClient(BINANCE_ETH_USDT_TICKER_SYMBOL)

    async def run_forever(self):
        await self.binance_client.connect_forever()
