import asyncio
import time

from client.models.Requests import TransactionFeeRequest
from client.models.Response import TransactionsDTO, TransactionFeeResponse


class TransactionFeeClient:
    def __init__(self) -> None:
        self.retry_times = 3

    async def get_fee(self, txnHash: str) -> TransactionsDTO:
        response = TransactionsDTO(transactionHash=txnHash)
        # TODO: implementation
        await asyncio.sleep(1)
        return response

    async def get_fees(self, txnHashList: list[str]) -> TransactionFeeResponse:
        transactionsList = await asyncio.gather(*[self.get_fee(txnHash) for txnHash in txnHashList])
        return TransactionFeeResponse(transactionList=transactionsList)

