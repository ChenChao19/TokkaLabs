import asyncio
import websockets
import json
from abc import ABC, abstractmethod
import logging

class AbstractBinanceWebSocketClient(ABC):
    BASE_WS_URL = "wss://stream.binance.com:9443/ws"
    MAX_RECONNECTS = 5
    RECONNECT_DELAY = 2  # Base delay in seconds for exponential backoff

    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
        self.reconnect_attempts = 0

    async def connect(self):
        """Attempt to connect to Binance WebSocket with reconnection logic."""
        while self.reconnect_attempts < self.MAX_RECONNECTS:
            try:
                stream_url = f"{self.BASE_WS_URL}/{self.symbol}@ticker"
                async with websockets.connect(stream_url) as websocket:
                    logging.info(f"Connected to {stream_url}")
                    self.reconnect_attempts = 0  # Reset on successful connection
                    await self._handle_messages(websocket)
            except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.InvalidURI) as e:
                logging.info(f"Connection lost: {e}")
                await self._reconnect()
            except Exception as e:
                logging.info(f"Unexpected error: {e}")
                break

    async def _handle_messages(self, websocket):
        """Receive and handle messages from the WebSocket."""
        async for message in websocket:
            data = json.loads(message)
            await self.process_message(data)

    async def _reconnect(self):
        """Handles reconnection with exponential backoff."""
        self.reconnect_attempts += 1
        delay = self.RECONNECT_DELAY * (2 ** (self.reconnect_attempts - 1))
        logging.info(f"Reconnecting in {delay} seconds... (Attempt {self.reconnect_attempts}/{self.MAX_RECONNECTS})")
        await asyncio.sleep(delay)

    @abstractmethod
    async def process_message(self, data):
        """Abstract method to process incoming WebSocket messages."""
        pass