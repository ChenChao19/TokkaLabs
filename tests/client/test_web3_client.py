import pytest

from core.client.AsyncWeb3Client import EvmClient

@pytest.mark.asyncio
class TestEvmClient:

    @pytest.fixture
    def evm_client(self):
        return EvmClient()

    @pytest.fixture
    def mock_infura(self, mocker):
        mocker.patch("os.getenv", return_value="https://mainnet.infura.io/v3/fake_key")

    @pytest.fixture
    def mock_transfer_event(self, mocker):
        return {
            "topics": [
                b"\xdd\xf9\xf9\x77\xfc\x17\x0a\x69\x00\xbb\x3f\x33\x77\xbb\x42\xf9",
                b"0x0000000000000000000000000000000000000000000000000000000000000001",
                b"0x0000000000000000000000000000000000000000000000000000000000000002",
            ],
            "data": b"",
        }

    @pytest.mark.asyncio
    async def test_get_eth_from_wei(self, evm_client):
        wei_value = 1000000000000000000  # 1 ETH in Wei
        eth_value = await evm_client.get_eth_from_wei(wei_value)
        assert eth_value == 1.0, "1 ETH in Wei should be converted to 1.0 Ether"

    @pytest.mark.asyncio
    async def test_verify_transaction_receipt_invalid_event(self, evm_client, mocker):
        txn_receipt = {
            "logs": [{
                "topics": [b"random_event_signature", b"0x123", b"0x456"],
                "data": b""
            }]
        }

        result = await evm_client.verify_transaction_receipt(txn_receipt)
        assert result is False, "Transaction should not be verified with an invalid event signature"

