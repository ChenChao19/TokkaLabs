from abc import ABC
from tests import RedisClient

# Open for extension, for now not much use
class BaseLoader(ABC):
    def __init__(self):
        self.redis = RedisClient()

