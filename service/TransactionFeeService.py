import asyncio
import json
import logging

from client.AsyncBinanceAPIClient import BinanceClient
from client.AsyncRedisClient import RedisClient
from service.models.Response import TransactionsDTO, TransactionFeeResponse
from util.consts import REDIS_NAME_TRANSACTION, REDIS_BINANCE_SPOT_DATA, REDIS_CHANNEL_TRANSACTION, \
    BINANCE_ETH_USDT_TICKER_SYMBOL_CAP
from util.util import is_valid_txn_hash

class TransactionFeeService:
    """
    Transaction Fee Service, based on the transaction hashes provided,
    Try to find the fee in USDT, if it cannot be found, schedule it for searching
    """
    def __init__(self) -> None:
        self.retry_times = 3
        self.redis = RedisClient()
        self.binance_client = BinanceClient()

    async def get_fee(self, txnHash: str) -> TransactionsDTO:
        response = TransactionsDTO(transactionHash=txnHash)
        if not is_valid_txn_hash(txnHash):
            response.error_msg = "Hash Invalid"
            return response

        transaction = await self.redis.hget_json(REDIS_NAME_TRANSACTION, txnHash)
        if not transaction or not transaction.get('timestamp'):
            response.error_msg = "Transaction not found, scheduled, try again later"
            await self.redis.publish_to_channel(REDIS_CHANNEL_TRANSACTION, txnHash)
            return response
        
        logging.info(f"get fee transaction found for hash: {txnHash}, transaction: {transaction}")
        timestamp = transaction.get('timestamp')

        eth_usdt_price = await self.redis.hget_json(REDIS_BINANCE_SPOT_DATA, timestamp)
        if not eth_usdt_price:
            eth_usdt_price = await self.binance_client.get_second_level_closing_price(BINANCE_ETH_USDT_TICKER_SYMBOL_CAP, timestamp * 1000)
            await self.redis.hset_json(REDIS_BINANCE_SPOT_DATA, timestamp, eth_usdt_price)

        logging.info(f"get fee eth_usdt_price price found for hash: {txnHash}, timestamp: {timestamp}, eth_usdt_price: {eth_usdt_price}")
        response.fee = round(float(eth_usdt_price) * float(transaction.get('gas')), 4)
        response.success = True
        return response

    async def get_fees(self, txnHashList: list[str]) -> TransactionFeeResponse:
        transactionsList = await asyncio.gather(*[self.get_fee(txnHash) for txnHash in txnHashList])
        return TransactionFeeResponse(transactionList=transactionsList)

