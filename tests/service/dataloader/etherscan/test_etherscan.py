import pytest
from unittest import mock

from core.service.dataLoader.etherscan.etherscan import EtherscanLoader


@pytest.fixture
def etherscan_loader():
    return EtherscanLoader()


@pytest.mark.asyncio
async def test_get_latest_block_number(etherscan_loader):
    with mock.patch.object(etherscan_loader.evm_client, "get_latest_block_number", return_value=100):
        latest_block = await etherscan_loader.get_latest_block_number()
        assert latest_block == 100


@pytest.mark.asyncio
async def test_get_block_range(etherscan_loader):
    etherscan_loader.last_processed_block = 95
    with mock.patch.object(etherscan_loader, "get_latest_block_number", return_value=100):
        start, end = await etherscan_loader.get_block_range()
        assert start == 96
        assert end == 100


@pytest.mark.asyncio
async def test_process_transaction(etherscan_loader):
    transaction = {"hash": "0x123", "gasUsed": 21000, "gasPrice": 100, "timeStamp": 1639532580}
    with mock.patch.object(etherscan_loader.evm_client, "get_eth_from_wei", return_value=0.0021) as mock_eth_from_wei, \
            mock.patch.object(etherscan_loader.redis, "hset_json", return_value=None) as mock_hset_json:
        await etherscan_loader.process_transaction(transaction)

        mock_eth_from_wei.assert_called_once_with(21000 * 100)
        mock_hset_json.assert_called_once_with("transactions", "0x123",
                                               {"timestamp": 1639532580, "gas": 0.0021})


@pytest.mark.asyncio
async def test_get_transactions_and_write_redis(etherscan_loader):
    transactions = [{"hash": "0x123", "gasUsed": 21000, "gasPrice": 100, "timeStamp": 1639532580}]
    etherscan_loader.last_processed_block = 90
    with mock.patch.object(etherscan_loader, "get_block_range", return_value=(91, 100)), \
            mock.patch.object(etherscan_loader.etherscan_client, "get_token_transfer_event_by_address",
                              return_value={"result": transactions}), \
            mock.patch.object(etherscan_loader, "process_transaction", return_value=None) as mock_process_transaction:
        await etherscan_loader.get_transactions_and_write_redis()
        mock_process_transaction.assert_called_once_with(transactions[0])
        assert etherscan_loader.last_processed_block == 100


def test_shutdown(etherscan_loader):
    etherscan_loader.shutdown()
    assert etherscan_loader.stop_event.is_set()
