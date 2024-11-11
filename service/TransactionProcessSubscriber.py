import asyncio
import json
import logging
from abc import ABC

from web3.types import TxReceipt

from client.AsyncRedisClient import RedisClient
from util.consts import REDIS_CHANNEL_TRANSACTION, REDIS_NAME_TRANSACTION
from client.AsyncWeb3Client import EvmClient


class TransactionProcessSubscriber(ABC):
    def __init__(self):
        self.stop_event = asyncio.Event()
        self.w3_client = EvmClient()
        self.redis = RedisClient()
        self.pubsub = None

    async def init(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(REDIS_CHANNEL_TRANSACTION)
        self.pubsub = pubsub
        logging.info(f"subscribed to channel {REDIS_CHANNEL_TRANSACTION}")

    async def run_forever(self):
        await self.init()
        logging.info("Get transactions and write redis")
        while not self.stop_event.is_set():
            msg = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
            if not msg:
                await asyncio.sleep(1)
                continue
            txn_hash = json.loads(msg['data'].decode())
            logging.info(f"Received message: {msg}, {txn_hash=}")
            await self.process_hash(txn_hash)

    async def process_hash(self, txn_hash: str):
        txn_receipt = await self.w3_client.get_transaction_receipt(txn_hash)
        is_valid_transaction = await self.w3_client.verify_transaction_receipt(
            txn_receipt
        )
        if is_valid_transaction:
            await self.process_valid_hash(txn_hash, txn_receipt)
        else:
            await self.process_invalid_hash(txn_hash)

    async def process_valid_hash(self, txn_hash: str, txn_receipt: TxReceipt):
        gas_used = int(txn_receipt["gasUsed"])
        gas_price = float(await self.w3_client.get_eth_from_wei(txn_receipt["effectiveGasPrice"]))
        block = await self.w3_client.w3.eth.get_block(txn_receipt["blockNumber"])
        timestamp = block["timestamp"]
        gas_in_eth = gas_used * gas_price
        processed = {
            "timestamp": timestamp,
            "gas": gas_in_eth
        }
        await self.redis.hset_json(REDIS_NAME_TRANSACTION, txn_hash, processed)
        logging.info(f"process txn_hash {txn_hash=}, {gas_in_eth=}")

    async def process_invalid_hash(self, txn_hash: str):
        """
        Hash invalid
        """
        await self.redis.hset_json(REDIS_NAME_TRANSACTION, txn_hash, 0)


