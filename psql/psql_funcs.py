from abc import ABC, abstractmethod
import psycopg2
# for localhost (sets secret values)
import set_env_values


class AbstractRedis(ABC):
    @abstractmethod
    def add_user(self):
        pass


class Redis(AbstractRedis):
    def __init__(self, psql_url: str):
        self.psql = psycopg2.connect(psql_url)
        self.cursor = self.psql.cursor()

    def add_user(self):
        self.cursor


if __name__ == '__main__':
    redis = Redis(os.getenv('REDIS_URL'))
    redis.all_keys()

