import os
from typing import Optional

import dotenv
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.exceptions import TransactionNotFound
from web3.types import TxReceipt

from tests import ETH_BUFFER_BLOCK, UNISWAP_V3_ETH_USDC_POOL_ADDR


class EvmClient:
    """
    Async Evm Client
    """

    def __init__(self):
        dotenv.load_dotenv()
        url = os.getenv("INFURA_RPC_URL")
        self.w3 = AsyncWeb3(AsyncHTTPProvider(url))
        self.transfer_event_sig = self.w3.keccak(
            text="Transfer(address,address,uint256)"
        ).hex()

    async def get_latest_block_number(self) -> int:
        latest_block = await self.w3.eth.get_block("latest")
        return latest_block["number"] - ETH_BUFFER_BLOCK

    async def get_eth_from_wei(self, wei: int) -> float:
        return float(self.w3.from_wei(wei, "ether"))

    async def get_transaction_receipt(self, txn_hash: str) -> Optional[TxReceipt]:
        try:
            txn_receipt = await self.w3.eth.get_transaction_receipt(txn_hash)
            return txn_receipt
        except TransactionNotFound:
            return None

    async def verify_transaction_receipt(self, txn_receipt: TxReceipt) -> bool:
        if not txn_receipt or not txn_receipt.get("logs"):
            return False
        for log in txn_receipt.get("logs"):
            if log["topics"][0].hex() != self.transfer_event_sig:
                continue
            from_address = self.w3.to_checksum_address(
                "0x" + log["topics"][1].hex()[24:]
            )
            to_address = self.w3.to_checksum_address(
                "0x" + log["topics"][2].hex()[24:]
            )
            if (
                    from_address == UNISWAP_V3_ETH_USDC_POOL_ADDR
                    or to_address == UNISWAP_V3_ETH_USDC_POOL_ADDR
            ):
                return True
        return False