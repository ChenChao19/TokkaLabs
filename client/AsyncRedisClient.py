import json
from aioredis import Redis
from util.consts import REDIS_HOST, REDIS_PORT, ONE_YEAR_IN_SECONDS


class RedisClient(Redis):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, **kwargs):
        super().__init__(host=host, port=port, **kwargs)

    async def publish_to_channel(self, channel: str, msg):
        return await self.publish(channel, json.dumps(msg))

    async def hset_json(self, name, key, value):
        await self.hset(name, key, json.dumps(value))
        return await self.expire(key, ONE_YEAR_IN_SECONDS)

    async def hget_json(self, name, key):
        obj = await self.hget(name, key)
        return json.loads(obj) if obj is not None else obj