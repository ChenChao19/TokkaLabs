import httpx

class EtherscanClient:
    """
    Async Etherscan API Client
    """
    BASE_URL = 'https://api.etherscan.io/api'

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
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()