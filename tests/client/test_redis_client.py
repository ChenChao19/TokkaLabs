import pytest
import json
from unittest import mock

from core.client.AsyncRedisClient import RedisClient
from core.util.consts import ONE_YEAR_IN_SECONDS


@pytest.mark.asyncio
async def test_publish_to_channel():
    channel = "test_channel"
    message = {"key": "value"}

    with mock.patch.object(RedisClient, 'publish', new_callable=mock.AsyncMock) as mock_publish:
        redis_client = RedisClient()

        await redis_client.publish_to_channel(channel, message)

        mock_publish.assert_called_once_with(channel, json.dumps(message))


@pytest.mark.asyncio
async def test_hset_json():
    name = "my_hash"
    key = "my_key"
    value = {"field": "value"}

    with mock.patch.object(RedisClient, 'hset', new_callable=mock.AsyncMock) as mock_hset, \
            mock.patch.object(RedisClient, 'expire', new_callable=mock.AsyncMock) as mock_expire:
        redis_client = RedisClient()

        await redis_client.hset_json(name, key, value)

        mock_hset.assert_called_once_with(name, key, json.dumps(value))

        mock_expire.assert_called_once_with(key, ONE_YEAR_IN_SECONDS)


@pytest.mark.asyncio
async def test_hget_json():
    name = "my_hash"
    key = "my_key"
    mock_obj = '{"field": "value"}'

    with mock.patch.object(RedisClient, 'hget', new_callable=mock.AsyncMock) as mock_hget:
        redis_client = RedisClient()

        mock_hget.return_value = mock_obj

        result = await redis_client.hget_json(name, key)

        mock_hget.assert_called_once_with(name, key)

        assert result == {"field": "value"}


@pytest.mark.asyncio
async def test_hget_json_key_not_found():
    name = "my_hash"
    key = "missing_key"

    with mock.patch.object(RedisClient, 'hget', new_callable=mock.AsyncMock) as mock_hget:
        redis_client = RedisClient()

        mock_hget.return_value = None

        result = await redis_client.hget_json(name, key)

        mock_hget.assert_called_once_with(name, key)

        assert result is None
