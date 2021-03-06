import jwt
import time
from abc import ABC, abstractmethod
from heroku_redis.redis_funcs import Redis


class AbstractJWT(ABC):
    @abstractmethod
    def create_token(self, user_id: int, token_ttl_sec: int) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass

    @abstractmethod
    def check_token(self, token: str) -> bool:
        pass


class JWT(AbstractJWT):
    def __init__(self, jwt_key: str, algorithm: str):
        self.__jwt_key = jwt_key
        self.__algorithm = algorithm

    def create_token(self, user_id: int, token_ttl_sec: int) -> str:
        json = {
            "user_id": user_id,
            "ttl": int(time.time()) + token_ttl_sec
        }
        return jwt.encode(json, self.__jwt_key, self.__algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return {
                "result": True,
                "message": "token was successfully docoded",
                "decoded_token": jwt.decode(token, self.__jwt_key, self.__algorithm)
            }
        except Exception as e:
            return {
                "result": False,
                "message": e,
            }

    def check_token(self, token: str) -> bool:
        resp = self.decode_token(token)
        if resp['result']:
            if 'ttl' in resp['decoded_token'] and resp['decoded_token']['ttl'] > int(time.time()):
                return True
        else:
            return False


if __name__ == '__main__':
    import set_env_values
    import os
    test = JWT(os.getenv('JWT_KEY'), os.getenv('JWT_ALGORITHM'))

    print(int(time.time()))
    token_1 = test.create_token(1, 20)
    print(token_1)
    print(test.decode_token(token_1))

