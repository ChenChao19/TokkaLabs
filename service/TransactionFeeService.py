import asyncio

from service.models.Response import TransactionsDTO, TransactionFeeResponse


class TransactionFeeService:
    """
    Transaction Fee Service, based on the transaction hashes provided,
    Try to find the fee in USDT, if it cannot be found, schedule it for searching
    """
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

