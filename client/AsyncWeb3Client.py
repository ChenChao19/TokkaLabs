import os
import dotenv
from web3 import AsyncHTTPProvider, AsyncWeb3

from util.consts import ETH_BUFFER_BLOCK


class EvmClient:
    """
    Async Evm Client
    """

    def __init__(self):
        dotenv.load_dotenv()
        url = os.getenv("RPC_URL")
        self.w3 = AsyncWeb3(AsyncHTTPProvider(url))

    async def get_latest_block_number(self) -> int:
        latest_block = await self.w3.eth.get_block("latest")
        return latest_block["number"] - ETH_BUFFER_BLOCK

    async def get_eth_from_wei(self, wei: int) -> float:
        return float(self.w3.from_wei(wei, "ether"))