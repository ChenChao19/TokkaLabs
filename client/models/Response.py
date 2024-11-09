from pydantic import BaseModel, Field

class TransactionsDTO(BaseModel):
    transactionHash: str = Field(..., description="Transaction Hash")
    success: str = Field(False, description="If a transaction fee can be calculated")
    fee: float = Field(0, description="Fee in USDT")
    error_msg: str = Field("", description="Error Message If fee cannot be calculated")

class TransactionFeeResponse(BaseModel):
    transactionList: list[TransactionsDTO]