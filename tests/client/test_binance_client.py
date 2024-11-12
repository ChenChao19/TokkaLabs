import pytest
from unittest.mock import patch

from core.client.AsyncBinanceAPIClient import BinanceClient


@pytest.mark.asyncio
async def test_get_second_level_closing_price_success():
    mock_response_data = [[1609459200000, 29000.0, 29100.0, 28900.0, 29050.0, 1000, 1609459201000]]

    with patch.object(BinanceClient, '_request', return_value=mock_response_data):
        client = BinanceClient()
        price = await client.get_second_level_closing_price("BTCUSDT", 1609459200000)
        assert price == 29050.0
