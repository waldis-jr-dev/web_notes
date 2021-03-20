import redis as redis_lib
from abc import ABC, abstractmethod
from typing import Dict
import time


class AbstractRedis(ABC):
    @abstractmethod
    def all_keys(self):
        pass

    @abstractmethod
    def add_token(self, encoded_token: dict, token: str) -> Dict[str, bool]:
        pass

    @abstractmethod
    def get_token(self, encoded_token: dict, token: str) -> Dict[str, bool]:
        pass

    @abstractmethod
    def delete_old_tokens(self):
        pass


class Redis(AbstractRedis):
    def __init__(self, redis_url: str):
        self.redis = redis_lib.Redis.from_url(redis_url)

    def all_keys(self):
        return self.redis.keys()

    def add_token(self, key: str, value: str) -> Dict[str, bool]:
        redis_resp = self.redis.set(key, value)
        if redis_resp:
            return {'result': True,
                    'message': 'token added successfully'
                    }
        else:
            return {'result': False,
                    'message': 'sth goes wrong'
                    }

    def delete_token(self, token_key):
        return self.redis.delete(token_key)

    def get_token(self, key: str) -> str:
        return self.redis.get(key)

    def delete_old_tokens(self):
        for key in self.redis.keys():
            key_as_str = str(key, encoding='UTF-8').split('.')
            if len(key_as_str) == 3 and int(key_as_str[1]) < int(time.time()):
                self.redis.delete(key)


if __name__ == '__main__':
    import os
    import set_env_values

    redis = Redis(os.getenv('REDIS_URL'))

    print(redis.all_keys())
    print(len(redis.all_keys()))
