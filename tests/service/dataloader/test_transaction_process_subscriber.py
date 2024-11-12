import pytest
from unittest import mock

from core.service.TransactionProcessSubscriber import TransactionProcessSubscriber


@pytest.fixture
def transaction_process_subscriber():
    return TransactionProcessSubscriber()


@pytest.mark.asyncio
async def test_init(transaction_process_subscriber):
    with mock.patch.object(transaction_process_subscriber.redis, "pubsub") as mock_pubsub:
        mock_pubsub.return_value.subscribe = mock.AsyncMock()

        await transaction_process_subscriber.init()

        mock_pubsub.return_value.subscribe.assert_called_once_with("transaction_channel")
        assert transaction_process_subscriber.pubsub is not None

@pytest.mark.asyncio
async def test_process_hash_valid_transaction(transaction_process_subscriber):
    txn_hash = "0x123"
    mock_txn_receipt = mock.Mock()

    with mock.patch.object(transaction_process_subscriber.w3_client, "get_transaction_receipt",
                           return_value=mock_txn_receipt), \
            mock.patch.object(transaction_process_subscriber.w3_client, "verify_transaction_receipt",
                              return_value=True), \
            mock.patch.object(transaction_process_subscriber, "process_valid_hash") as mock_process_valid:
        await transaction_process_subscriber.process_hash(txn_hash)

        mock_process_valid.assert_called_once_with(txn_hash, mock_txn_receipt)


@pytest.mark.asyncio
async def test_process_hash_invalid_transaction(transaction_process_subscriber):
    txn_hash = "0x123"
    mock_txn_receipt = mock.Mock()

    with mock.patch.object(transaction_process_subscriber.w3_client, "get_transaction_receipt",
                           return_value=mock_txn_receipt), \
            mock.patch.object(transaction_process_subscriber.w3_client, "verify_transaction_receipt",
                              return_value=False), \
            mock.patch.object(transaction_process_subscriber, "process_invalid_hash") as mock_process_invalid:
        await transaction_process_subscriber.process_hash(txn_hash)

        mock_process_invalid.assert_called_once_with(txn_hash)


@pytest.mark.asyncio
async def test_process_valid_hash(transaction_process_subscriber):
    txn_hash = "0x123"
    txn_receipt = {
        "gasUsed": "21000",
        "effectiveGasPrice": "20000000000",
        "blockNumber": 123456
    }
    block_data = {"timestamp": 1670000000}
    expected_gas_in_eth = 21000 * float(20)

    with mock.patch.object(transaction_process_subscriber.w3_client.w3.eth, "get_block", return_value=block_data), \
            mock.patch.object(transaction_process_subscriber.redis, "hset_json") as mock_hset_json, \
            mock.patch.object(transaction_process_subscriber.w3_client, "get_eth_from_wei", return_value=20):
        await transaction_process_subscriber.process_valid_hash(txn_hash, txn_receipt)

        processed_data = {
            "timestamp": block_data["timestamp"],
            "gas": expected_gas_in_eth
        }

        mock_hset_json.assert_called_once_with("transactions", txn_hash, processed_data)


@pytest.mark.asyncio
async def test_process_invalid_hash(transaction_process_subscriber):
    txn_hash = "0x123"

    with mock.patch.object(transaction_process_subscriber.redis, "hset_json") as mock_hset_json:
        await transaction_process_subscriber.process_invalid_hash(txn_hash)

        mock_hset_json.assert_called_once_with("transactions", txn_hash, 0)
