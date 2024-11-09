from pydantic import BaseModel

class TransactionFeeRequest(BaseModel):
    transactionHashes: list[str]