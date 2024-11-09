import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aioredis import Redis
import os


# Initialize FastAPI app
app = FastAPI()

# Get Redis connection details from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

# Connect to Redis
r = Redis(host=REDIS_HOST, port=REDIS_PORT)

# Define a data model for the request body
class TransactionFee(BaseModel):
    tx_hash: str
    fee_in_eth: float
    fee_in_usdt: float

# Endpoint to store transaction fee in Redis
@app.post("/store-fee/")
async def store_transaction_fee(transaction: TransactionFee):
    # Store the transaction fee in Redis using tx_hash as the key
    key = f"txn:{transaction.tx_hash}"
    await r.hmset(key, {
        "fee_in_eth": transaction.fee_in_eth,
        "fee_in_usdt": transaction.fee_in_usdt
    })
    return {"message": "Transaction fee stored successfully!"}

# Endpoint to retrieve transaction fee from Redis
@app.get("/get-fee/{tx_hash}")
async def get_transaction_fee(tx_hash: str):
    key = f"txn:{tx_hash}"
    txn_data = await r.hgetall(key)
    print(txn_data)

    if not txn_data:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Return the fee details
    return {
        # "tx_hash": tx_hash,
        # "fee_in_eth": float(txn_data["fee_in_eth"]),
        # "fee_in_usdt": float(txn_data["fee_in_usdt"])
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)