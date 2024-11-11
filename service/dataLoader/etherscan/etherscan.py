import asyncio
import logging
import os

from dotenv import load_dotenv

from client.AsyncEtherscanAPIClient import EtherscanClient
from client.AsyncWeb3Client import EvmClient
from service.dataLoader.BaseDataLoader import BaseLoader
from util.consts import ETHERSCAN_API_KEY, REDIS_NAME_TRANSACTION, UNISWAP_V3_ETH_USDC_POOL_ADDR


class EtherscanLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        load_dotenv()
        API_KEY = os.getenv(ETHERSCAN_API_KEY)
        self.etherscan_client = EtherscanClient(API_KEY)
        self.evm_client = EvmClient()
        self.last_processed_block = None
        self.stop_event = asyncio.Event()

    async def get_latest_block_number(self) -> int:
        latest_block = await self.evm_client.get_latest_block_number()
        return latest_block

    async def get_block_range(self):
        latest_block = await self.get_latest_block_number()
        if self.last_processed_block:
            start = min(latest_block, self.last_processed_block + 1)
        else:
            start = latest_block
        return start, latest_block

    async def process_transaction(self, txn: dict):
        txn_hash = str(txn["hash"]).lower()
        gas_used = int(txn["gasUsed"])
        gas_price = int(txn["gasPrice"])
        timestamp = int(txn["timeStamp"])
        cost_in_wei = gas_used * gas_price
        gas_in_eth = await self.evm_client.get_eth_from_wei(cost_in_wei)
        processed = {
            "timestamp": timestamp,
            "gas": gas_in_eth
        }
        await self.redis.hset_json(REDIS_NAME_TRANSACTION, txn_hash, processed)

    async def get_transactions_and_write_redis(self):
        start, end = await self.get_block_range()
        if start == self.last_processed_block:
            return
        page = 1
        offset = 10000
        resp = await self.etherscan_client.get_token_transfer_event_by_address(
            address=UNISWAP_V3_ETH_USDC_POOL_ADDR,
            page=page,
            offset=offset,
            start_block=start,
            end_block=end,
        )
        transactions = resp.get("result", [])
        await asyncio.gather(*[self.process_transaction(txn) for txn in transactions])
        self.last_processed_block = end

    async def run_forever(self):
        """Runs the loader indefinitely, processing new transactions as blocks update."""
        logging.info("EtherscanLoader Get transactions and write redis")
        while not self.stop_event.is_set():
            await self.get_transactions_and_write_redis()
            await asyncio.sleep(10)  # Adjust sleep time as needed

    def shutdown(self):
        """Signals the loader to stop processing."""
        self.stop_event.set()
        logging.info("Shutdown signal received, stopping EtherscanLoader...")
