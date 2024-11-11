import httpx
import asyncio
import logging

class BinanceClient:
    """
    Async Etherscan API Client with retry logic and timeout handling
    """
    BASE_URL = "https://api.binance.com/api/v3/klines"
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    TIMEOUT = 10  # seconds for httpx requests

    async def get_second_level_closing_price(
            self,
            symbol: str,
            epoch_milli: int,
            limit: int = 1
    ) -> float:
        params = {
            "symbol": symbol,
            "interval": "1s",
            "startTime": epoch_milli,
            "endTime": epoch_milli,
            "limit": limit
        }
        candle = await self._request(params)
        return candle[0][4]

    async def _request(self, params: dict) -> list[list]:
        attempt = 0
        while attempt < self.MAX_RETRIES:
            try:
                async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
                    response = await client.get(self.BASE_URL, params=params)
                    response.raise_for_status()  # Raise for HTTP errors
                    return response.json()
            except httpx.ReadTimeout:
                logging.warning(f"Request timed out. Attempt {attempt + 1}/{self.MAX_RETRIES}")
            except httpx.RequestError as exc:
                logging.warning(f"Request error: {exc}. Attempt {attempt + 1}/{self.MAX_RETRIES}")
            attempt += 1
            await asyncio.sleep(self.RETRY_DELAY * (2 ** (attempt - 1)))  # Exponential backoff

        raise httpx.ReadTimeout("Max retries exceeded for Binance API request.")
