from abc import ABC
from client.AsyncRedisClient import RedisClient


class BaseSubscriber(ABC):

    def __init__(self):
        self.redis = RedisClient()
