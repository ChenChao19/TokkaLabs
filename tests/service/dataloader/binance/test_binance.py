import pytest
from unittest import mock
from core.service.dataLoader.binance.binance import BinanceTickerClient, BinanceLoader

@pytest.fixture
def binance_ticker_client():
    return BinanceTickerClient(symbol="ethusdt")

@pytest.mark.asyncio
async def test_process_message(binance_ticker_client):
    with mock.patch.object(binance_ticker_client.redis, "hset_json", return_value=None) as mock_hset_json:
        data = {"E": 1639532580000, "c": "3000.45"}  # Example data
        await binance_ticker_client.process_message(data)

        mock_hset_json.assert_called_once_with("binance_spot_data", 1639532580, 3000.45)

@pytest.mark.asyncio
async def test_shutdown(binance_ticker_client):
    with mock.patch("logging.info") as mock_log_info:
        binance_ticker_client.shutdown()
        assert binance_ticker_client.stop is True
        mock_log_info.assert_called_with("Shutdown signal received, stopping BinanceTickerClient...")

@pytest.mark.asyncio
async def test_binance_loader_run_forever():
    binance_loader = BinanceLoader()

    with mock.patch.object(binance_loader.binance_client, "connect_forever", return_value=None) as mock_connect_forever:
        await binance_loader.run_forever()
        mock_connect_forever.assert_called_once()
