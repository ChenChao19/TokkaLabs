import httpx
import asyncio
import logging

class EtherscanClient:
    """
    Async Etherscan API Client with retry logic and timeout handling
    """
    BASE_URL = 'https://api.etherscan.io/api'
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    TIMEOUT = 10  # seconds for httpx requests

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_token_transfer_event_by_address(
            self,
            address: str,
            page: int = 1,
            offset: int = 100,
            start_block: int = 0,
            end_block: int = 99999999,
            sort: str = "asc"
    ) -> dict:
        params = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "page": page,
            "offset": offset,
            "startblock": start_block,
            "endblock": end_block,
            "sort": sort,
            "apikey": self.api_key,
        }
        return await self._request(params)

    async def _request(self, params: dict) -> dict:
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

        raise httpx.ReadTimeout("Max retries exceeded for Etherscan API request.")
