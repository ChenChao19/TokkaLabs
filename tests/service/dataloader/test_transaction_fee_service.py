import pytest
from unittest import mock

from core.service.TransactionFeeService import TransactionFeeService

@pytest.fixture
def transaction_fee_service():
    return TransactionFeeService()


@pytest.mark.asyncio
async def test_get_fee_invalid_hash(transaction_fee_service):
    with mock.patch("core.util.util.is_valid_txn_hash", return_value=False):
        response = await transaction_fee_service.get_fee("invalid_hash")
        assert response.error_msg == "Hash Invalid"
        assert response.success is False


@pytest.mark.asyncio
async def test_get_fee_transaction_not_found(transaction_fee_service):
    txn_hash = "0x7a1c4ceb50554622dc35a5618f2a490a7fc66ae5afc201526260f35411896f75"

    with mock.patch.object(transaction_fee_service.redis, "hget_json", return_value=None), \
            mock.patch.object(transaction_fee_service.redis, "publish_to_channel", return_value=None) as mock_publish:
        response = await transaction_fee_service.get_fee(txn_hash)

        mock_publish.assert_called_once_with("transaction_channel", txn_hash)
        assert response.error_msg == "Transaction not found, scheduled, try again later"
        assert response.success is False


@pytest.mark.asyncio
async def test_get_fee_success_with_cached_price(transaction_fee_service):
    txn_hash = "0x7a1c4ceb50554622dc35a5618f2a490a7fc66ae5afc201526260f35411896f75"
    transaction_data = {"timestamp": 1639532580, "gas": "0.01"}
    eth_usdt_price = "3000"

    with mock.patch.object(transaction_fee_service.redis, "hget_json", side_effect=[transaction_data, eth_usdt_price]):

        response = await transaction_fee_service.get_fee(txn_hash)
        print(response)

        expected_fee = round(float(eth_usdt_price) * float(transaction_data["gas"]), 4)
        assert response.fee == expected_fee
        assert response.success is True


@pytest.mark.asyncio
async def test_get_fee_success_with_fetched_price(transaction_fee_service):
    txn_hash = "0x7a1c4ceb50554622dc35a5618f2a490a7fc66ae5afc201526260f35411896f75"
    transaction_data = {"timestamp": 1639532580, "gas": "0.01"}
    fetched_price = "3000"

    with mock.patch.object(transaction_fee_service.redis, "hget_json", side_effect=[transaction_data, None]), \
            mock.patch.object(transaction_fee_service.binance_client, "get_second_level_closing_price",
                              return_value=fetched_price) as mock_binance, \
            mock.patch.object(transaction_fee_service.redis, "hset_json", return_value=None) as mock_hset:
        response = await transaction_fee_service.get_fee(txn_hash)

        mock_binance.assert_called_once()
        mock_hset.assert_called_once_with("binance_spot_data", transaction_data["timestamp"], fetched_price)

        expected_fee = round(float(fetched_price) * float(transaction_data["gas"]), 4)
        assert response.fee == expected_fee
        assert response.success is True
