import re

def is_valid_txn_hash(txn_hash: str) -> bool:
    return bool(re.match( r"^0x[a-fA-F0-9]{64}$", txn_hash))