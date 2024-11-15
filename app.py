import logging

import uvicorn
from fastapi import FastAPI

from core.service.TransactionFeeService import TransactionFeeService
from core.service.models.Requests import TransactionFeeRequest
from core.service.models.Response import TransactionFeeResponse
from core.util.logger import setup_logger

app = FastAPI()
transactionFeeService = TransactionFeeService()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | "
                           "%(module)s:%(funcName)s:%(lineno)d - %(message)s")

@app.post("/transaction-fee/", response_model=TransactionFeeResponse)
async def get_transaction_fee(transactionFeeRequest: TransactionFeeRequest):
    logging.info(f"get transaction fee, transactionFeeRequest: {transactionFeeRequest}")
    return await transactionFeeService.get_fees(transactionFeeRequest.transactionHashes)

if __name__ == "__main__":
    setup_logger("app.log")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True,log_level='debug')