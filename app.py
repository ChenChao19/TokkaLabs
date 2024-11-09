import uvicorn
from fastapi import FastAPI

from client.TransactionFeeClient import TransactionFeeClient
import logging

from client.models.Requests import TransactionFeeRequest
from client.models.Response import TransactionFeeResponse

app = FastAPI()
transactionFeeClient = TransactionFeeClient()

@app.post("/transaction-fee/", response_model=TransactionFeeResponse)
async def get_transaction_fee(transactionFeeRequest: TransactionFeeRequest):
    logging.info(f"get transaction fee, transactionFeeRequest: {transactionFeeRequest}")
    return await transactionFeeClient.get_fees(transactionFeeRequest.transactionHashes)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)