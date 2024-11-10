import uvicorn
import asyncio
from fastapi import FastAPI

from service.TransactionFeeService import TransactionFeeService
import logging

from service.models.Requests import TransactionFeeRequest
from service.models.Response import TransactionFeeResponse

app = FastAPI()
transactionFeeService = TransactionFeeService()

@app.post("/transaction-fee/", response_model=TransactionFeeResponse)
async def get_transaction_fee(transactionFeeRequest: TransactionFeeRequest):
    logging.info(f"get transaction fee, transactionFeeRequest: {transactionFeeRequest}")
    return await transactionFeeService.get_fees(transactionFeeRequest.transactionHashes)



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)