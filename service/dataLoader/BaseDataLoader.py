from abc import ABC
from client.AsyncRedisClient import RedisClient

# Open for extension, for now not much use
class BaseLoader(ABC):
    def __init__(self):
        self.redis = RedisClient()

