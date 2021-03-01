import redis
from abc import ABC, abstractmethod


class AbstractRedis(ABC):
    @abstractmethod
    def all_keys(self):
        pass


class Redis(AbstractRedis):
    def __init__(self, redis_url: str):
        self.redis = redis.Redis.from_url(redis_url)

    def all_keys(self):
        print(self.redis.keys())


if __name__ == '__main__':
    import os
    import set_env_values
    redis = Redis(os.getenv('REDIS_URL'))
    redis.all_keys()
